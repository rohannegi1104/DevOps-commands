import paramiko
import subprocess

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
    print("Retrieving Docker images from the source server...")
    command = "docker images"
    stdin, stdout, stderr = client.exec_command(command)
    images = stdout.read().decode()
    print("Docker images on source server:")
    print(images)
    return images

def check_image_on_server(server, image_name, username, password):
    command = f"sshpass -p '{password}' ssh {username}@{server} 'docker images -q {image_name}'"
    print(f"Checking for image: {image_name}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error checking image: {result.stderr.strip()}")
        return None
    else:
        if result.stdout.strip():
            print(f"Image {image_name} found with ID: {result.stdout.strip()}")
            return result.stdout.strip()  # Return the image ID
        else:
            print(f"Image {image_name} not found on server.")
            return None

def replicate_docker_images(source_server, destination_server, image_names, username, source_password, destination_password):
    try:
        for image_name in image_names:
            image_id = check_image_on_server(source_server, image_name, username, source_password)
            if not image_id:
                print(f"Skipping replication for {image_name}.")
                continue

            # Save and load the Docker image
            save_command = f"sshpass -p '{source_password}' ssh {username}@{source_server} 'docker save {image_name} | gzip'"
            load_command = f"sshpass -p '{destination_password}' ssh {username}@{destination_server} 'gzip -d | docker load'"
            ssh_command = f"{save_command} | {load_command}"

            print(f"Replicating image {image_name} from {source_server} to {destination_server}...")
            subprocess.run(ssh_command, shell=True, check=True)

            print(f"Image {image_name} replicated from {source_server} to {destination_server} successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during Docker image transfer: {e}")

if __name__ == "__main__":
    source_server = "190.168.8.186"
    destination_server = "190.168.8.189"
    image_names = [
        "plasmacomputing/microai:devicemgmtapi_release_4.2.0_2219",
        "plasmacomputing/microai:devicemgmtwebapp_release_4.2.0_2220"
    ]
    username = "c2m"
    source_password = "Plasma@321!"
    destination_password = "Plasma@123!"

    source_client = connect_to_server(source_server, username, source_password)
    if source_client:
        get_docker_images(source_client)
        source_client.close()

    replicate_docker_images(source_server, destination_server, image_names, username, source_password, destination_password)