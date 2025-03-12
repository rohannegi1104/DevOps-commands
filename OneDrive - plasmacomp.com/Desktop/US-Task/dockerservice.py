import subprocess

#service name
service_name = input("Enter the service name: ")

#command to deploy the application through dockerswarm
docker_command = ["docker", "service", "create", "--name", service_name, "--mount", "type=bind,source=/root/Jenkins,target=/app", "--replicas", "2",
                  "--publish", "8087:80", "plasmacomputing/microai:devicemgmtapi_release_4.2.0_2216"]


#file handling concept
try:
    subprocess.run(docker_command, check=True)
    print(f"Service '{service_name}' created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error creating service '{service_name}'")