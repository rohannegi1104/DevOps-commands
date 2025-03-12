import subprocess
import getpass
import requests

# Function to run shell commands
def run(command):
    print(f"Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Command output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}")
        return None

# Function to log in to Docker Hub
def login_dockerhub(username, password):
    print(f"Logging in to Docker Hub as {username}...")
    login_command = f'echo "{password}" | docker login -u "{username}" --password-stdin'
    if run(login_command) is None:
        print("Login failed!")
        exit(1)
    print("Login successful!")

# Function to get a list of Docker images from the VM server
def list_docker_images():
    print("Retrieving list of local Docker images from the VM server...")
    output = run("docker images --format '{{.Repository}}:{{.Tag}}'")
    if output:
        images = output.split("\n")
        valid_images = [img for img in images if "<none>" not in img]
        print(f"Found {len(valid_images)} valid local images on the VM server.")
        return valid_images
    print("No valid images found on the VM server.")
    return []

# Function to check if the image exists on Docker Hub
def check_image_on_dockerhub(image):
    print(f"Checking if image {image} exists on Docker Hub...")
    # Split by the last colon, in case the repo name contains a colon (e.g., "some/repo:tag")
    try:
        repo, tag = image.rsplit(":", 1)
    except ValueError:
        print(f"Error: Image '{image}' does not have a valid format. Skipping...")
        return False

    url = f"https://hub.docker.com/v2/repositories/{repo}/tags/{tag}/"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Image {image} already exists on Docker Hub. Skipping...")
            return True
        elif response.status_code == 404:
            print(f"Image {image} not found on Docker Hub.")
            return False
        else:
            print(f"Error with {image}: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Error checking {image}: {e}")
        return False

# Function to tag and push images that do not exist on Docker Hub
def tag_and_push(images, username):
    for image in images:
        print(f"Processing image: {image}")
        try:
            repo, tag = image.rsplit(":", 1)  # Handle the case where the image has multiple colons
        except ValueError:
            print(f"Error: Image '{image}' does not have a valid format. Skipping...")
            continue
        
        # We keep the same tag; no need to add the username prefix
        new_tag = image  # Using the same tag and repo

        # Check if the image already exists on Docker Hub
        if check_image_on_dockerhub(new_tag):
            continue  # Skip if the image already exists on Docker Hub
        
        # Tag the image with the same tag (no change)
        print(f"Tagging {image} as {new_tag}...")
        if run(f"docker tag {image} {new_tag}") is None:
            print(f"Failed to tag {image}.")
            continue
        
        # Push the image to Docker Hub
        print(f"Pushing {new_tag} to Docker Hub...")
        result = run(f"docker push {new_tag}")
        
        if result is None:
            print(f"Failed to push {new_tag}. This could be due to permission issues or other errors.")
        elif "denied: requested access to the resource is denied" in result:
            print(f"Permission denied for image {new_tag}. Skipping...")
        else:
            print(f"Successfully pushed {new_tag}.")

def main():
    username = input("Enter your Docker Hub username: ")
    password = getpass.getpass("Enter your Docker Hub password: ")

    login_dockerhub(username, password)

    images = list_docker_images()

    if not images:
        print("No images found to check or push.")
        return

    tag_and_push(images, username)

    print("Process completed.")

if __name__ == "__main__":
    main()
