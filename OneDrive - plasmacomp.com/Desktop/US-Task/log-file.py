import docker
import logging

# Set up logging to overwrite the file each time
logging.basicConfig(filename='docker_actions.log', level=logging.INFO, filemode='w')

client = docker.from_env()

# List all containers and log their status
for container in client.containers.list(all=True):
    logging.info(f"Container: {container.name}, Status: {container.status}")
