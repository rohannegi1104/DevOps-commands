import subprocess
import getpass
import os

print("Updating and installing Docker and authentication tools...")
subprocess.run(["sudo", "apt", "update", "-y"], check=True)
subprocess.run(["sudo", "apt", "install", "apache2-utils", "-y"], check=True)

print("Checking Docker version...")
subprocess.run(["sudo", "docker", "--version"], check=True)

registry_folder = "/opt/docker_registry"
auth_folder = "/opt/docker_registry_auth"
os.makedirs(registry_folder, exist_ok=True)
os.makedirs(auth_folder, exist_ok=True)

username = "rohan"
password = getpass.getpass("Enter password for private registry login: ")

password_file_path = os.path.join(auth_folder, "password_file")

try:
    print("Creating password file for registry login...")
    subprocess.run(
        ["htpasswd", "-i", "-Bc", password_file_path, username],
        input=password, text=True, check=True
    )
except subprocess.CalledProcessError as e:
    print(f"Error creating password file: {e}")
    exit(1)

print("Starting the private Docker registry...")
subprocess.run([
    "sudo", "docker", "run", "-d", "--restart", "always", "-p", "5000:5000",
    "-v", f"{registry_folder}:/var/lib/registry",
    "-v", f"{auth_folder}:/auth",
    "-e", "REGISTRY_AUTH=htpasswd",
    "-e", "REGISTRY_AUTH_HTPASSWD_REALM=RegistryRealm",
    "-e", f"REGISTRY_AUTH_HTPASSWD_PATH=/auth/password_file",
    "registry:2"
], check=True)

image_name = "hello-world"
print(f"Pulling the {image_name} image from Docker Hub...")
subprocess.run(["sudo", "docker", "pull", image_name], check=True)

private_registry_image = "190.168.8.189:5000/hello-world:latest"
print(f"Tagging the {image_name} image for the private registry...")
subprocess.run(["sudo", "docker", "tag", image_name, private_registry_image], check=True)

print("Logging into the private registry...")
subprocess.run(
    ["sudo", "docker", "login", "190.168.8.189:5000", "-u", username, "--password-stdin"],
    input=password, text=True, check=True
)

print(f"Pushing the {image_name} image to the private registry...")
subprocess.run(["sudo", "docker", "push", private_registry_image], check=True)

print("Creating a container from the pushed image...")
subprocess.run(
    f"sudo docker run -d -p 5001:5000 {private_registry_image}",
    shell=True, check=True
)

print("Private Docker registry setup and image push complete.")