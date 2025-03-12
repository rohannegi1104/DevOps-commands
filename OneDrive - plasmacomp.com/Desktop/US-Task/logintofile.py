import docker
import logging

logging.basicConfig(filename='docker_logs.log', level=logging.INFO)

client = docker.from_env()

logging.info("Container Logs:")
for container in client.containers.list(all=True):
    logging.info(f"Container Name: {container.name}, Status: {container.status}, ID: {container.id}")

logging.info("\nImage Logs:")
for image in client.images.list():
    logging.info(f"Image: {', '.join(image.tags)}, ID: {image.id}")
