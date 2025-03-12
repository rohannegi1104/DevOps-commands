import paramiko

#my cred
my_ip = '190.168.8.189'
my_username = 'c2m'
my_pass = 'Plasma@123!'

#frnd cred
frnd_ip = '190.168.8.186'
frnd_username = 'c2m'
frnd_pass = 'Plasma@321!'

# Docker images to replicate
images_to_replicate = [
    'plasmacomputing/microai:devicemgmtapi_release_4.2.0_2219',
    'plasmacomputing/microai:devicemgmtwebapp_release_4.2.0_2220'
]

#establishes ssh connectiom
def connect_to_server(ip, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)
        print(f"Successfully connected to {ip}")
        return client
    except Exception as e:
        print(f"Error connecting to {ip}: {e}")
        return None

#list of docker images of frnd server
def get_docker_images(client):
    stdin, stdout, stderr = client.exec_command("docker images")
    print("Docker Images on the friend's server ip is  198.168.8.186:")
    print(stdout.read().decode())
    print(stderr.read().decode())
     
my_server = connect_to_server(my_ip, my_username, my_pass)
frnd_server = connect_to_server(frnd_ip, frnd_username, frnd_pass)

if frnd_server:
    get_docker_images(frnd_server)

if my_server:
    my_server.close()
if frnd_server:
    frnd_server.close()