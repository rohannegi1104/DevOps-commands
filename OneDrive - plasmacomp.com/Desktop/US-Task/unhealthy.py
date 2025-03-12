import docker

client = docker.from_env()

# Restart unhealthy containers
for container in client.containers.list(all=True):
    if container.status == 'unhealthy':
        container.restart()
        print(f"Restarted: {container.name}")
