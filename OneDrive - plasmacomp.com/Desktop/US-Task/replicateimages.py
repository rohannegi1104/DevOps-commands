import paramiko

r#source
rohan_ip = '190.168.8.189'     
rohan_username = 'c2m'  
rohan_pass = 'Plasma@123!'  

#destination
vibhor_ip = '190.168.8.186'
vibhor_username = 'c2m'  
vibhor_pass = 'Plasma@321!'

#make connection between two server
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

#list of docker from destination ip
def get_docker_images(client):
    try:
        stdin, stdout, stderr = client.exec_command('docker images')
        output = stdout.read().decode()
        if output:
            print("Docker Images on the destination server:")
            print(output)
        error = stderr.read().decode()
        if error:
            print(f"Error: {error}")
    except Exception as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    rohan_server = connect_to_server(rohan_ip, rohan_username, rohan_pass)
    
    if rohan_server:
        vibhor_server = connect_to_server(vibhor_ip, vibhor_username, vibhor_pass)
        
        if vibhor_server:
            get_docker_images(vibhor_server)
            vibhor_server.close()
        
        rohan_server.close()