import docker

client = docker.from_env()

# Check if any container is restarting
if any(container.status == 'restarting' for container in client.containers.list(all=True)):
    print("Some containers are restarting.")
else:
    print("No containers are restarting.")
