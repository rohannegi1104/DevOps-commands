import paramiko

user_ip = '190.168.8.186'  
user_username = 'c2m'  
user_pass = 'Plasma@321!'  


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

def get_docker_images(client):
    try:
        stdin, stdout, stderr = client.exec_command('docker images')
        output = stdout.read().decode()
        if output:
            print("Docker Images on the source server:")
            print(output)
        error = stderr.read().decode()
        if error:
            print(f"Error: {error}")
    except Exception as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    user_client = connect_to_server(user_ip, user_username, user_pass)
    
    if user_client:
        get_docker_images(user_client)
        user_client.close()