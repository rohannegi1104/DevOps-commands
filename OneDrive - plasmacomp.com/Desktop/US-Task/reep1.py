import paramiko
import subprocess
import time
import os

# Server details
source_server_user = "c2m"
source_server_ip = "190.168.8.186"  # Source server
source_server_pass = 'Plasma@321!'

destination_server_user = "c2m"
destination_server_ip = "190.168.8.189"  # Destination server
destination_server_pass = 'Plasma@123!'

# List of Docker images to replicate
docker_images = [
    "plasmacomputing/microai:devicemgmtapi_release_4.2.0_2219",
    "plasmacomputing/microai:devicemgmtwebapp_release_4.2.0_2220"
]

def connect_to_server(ip, username, password):
    print(f"Connecting to server {ip} as user {username}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password)
        print(f"Connected to {ip} successfully.")
        return client
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
        return None

def get_docker_images(client):
    """the list of Docker images from the source server."""
    print("Retrieving Docker images from the source server...")
    command = "docker images"
    stdin, stdout, stderr = client.exec_command(command)
    images = stdout.read().decode()
    print("Docker images on source server:")
    print(images)

def save_docker_image(client, image_name, output_file):
    print(f"Saving Docker image '{image_name}' to '{output_file}' on the source server...")
    command = f"docker save -o {output_file} {image_name}"
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    error = stderr.read().decode()

    if error:
        print(f"Error saving image '{image_name}': {error}")
    else:
        print(f"Successfully saved image '{image_name}' to '{output_file}'.")

    time.sleep(1)

def check_docker_image_exists(client, image_name):
    print(f"Checking if Docker image '{image_name}' exists on the source server...")
    command = f"docker images -q {image_name}"
    stdin, stdout, stderr = client.exec_command(command)
    exists = bool(stdout.read().decode().strip())
    print(f"Docker image '{image_name}' exists: {exists}")
    return exists

def check_file_exists_on_server(client, file_path):
    print(f"Checking if file '{file_path}' exists on the source server...")
    command = f"test -f {file_path} && echo 'exists' || echo 'not exists'"
    stdin, stdout, stderr = client.exec_command(command)
    file_exists = stdout.read().decode().strip() == 'exists'
    print(f"File '{file_path}' exists: {file_exists}")
    return file_exists

def transfer_image_to_server(local_file, remote_user, remote_host):
    print(f"Transferring '{local_file}' to {remote_user}@{remote_host}...")
    command = f"scp {local_file} {remote_user}@{remote_host}:~/"
    print(f"Executing command: {command}")  # Debugging output
    result = subprocess.run(command, shell=True, capture_output=True)

    if result.returncode != 0:
        print(f"Error transferring file: {result.stderr.decode()}")
    else:
        print("File transferred successfully.")

def load_docker_image(client, remote_path):
    print(f"Loading Docker image from '{remote_path}' on the destination server...")
    command = f"docker load -i {remote_path}"
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    print(stdout.read().decode())
    print(stderr.read().decode())

def list_files_in_directory(client, directory):
    print(f"Listing files in directory '{directory}'...")
    command = f"ls -l {directory}"
    stdin, stdout, stderr = client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def main():
    print("Starting the Docker image replication process...")
    replication_directory = "/home/c2m/replication/"

    # Connect to the source server
    source_server = connect_to_server(source_server_ip, source_server_user, source_server_pass)

    if source_server:
        # Call the function to get and display Docker images
        get_docker_images(source_server)

        for image in docker_images:
            print(f"Processing image: {image}")

            if not check_docker_image_exists(source_server, image):
                print(f"Error: Docker image '{image}' does not exist on the source server. Skipping this image.")
                continue

            output_file_name = f"{image.replace('/', '_').replace(':', '_')}.tar"
            output_file = os.path.join(replication_directory, output_file_name)  # Path on the source server

            save_docker_image(source_server, image, output_file)

            # Check if the file was created on the source server
            if not check_file_exists_on_server(source_server, output_file):
                print(f"Error: The file {output_file} was not created. Skipping this image.")
                continue

            # Transfer the image to the control server (this server)
            transfer_image_to_server(output_file, destination_server_user, destination_server_ip)

            # Connect to the destination server to load the image
            destination_server = connect_to_server(destination_server_ip, destination_server_user, destination_server_pass)
            if destination_server:
                load_docker_image(destination_server, f"~/{output_file_name}")
                destination_server.close()

            print(f"Keeping local tar file '{output_file}'...")

        print("Docker images have been copied successfully.")

    if source_server:
        source_server.close()

if __name__ == "__main__":
    main()