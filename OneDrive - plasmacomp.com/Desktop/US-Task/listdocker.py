import docker

# Initialize the Docker client
client = docker.from_env()

# List and print running containers
for container in client.containers.list():
    print(container.name)
