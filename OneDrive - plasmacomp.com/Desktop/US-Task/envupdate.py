import os

def update_env_file(env_file, key, value):
    lines = []
    key_exists = False  

    if os.path.exists(env_file):  
        with open(env_file, 'r') as file:
            for line in file:
                if line.startswith(f"{key}="): 
                    line = f"{key}={value}\n"  
                    key_exists = True
                lines.append(line)  

    if not key_exists:
        lines.append(f"{key}={value}\n")  

    with open(env_file, 'w') as file:
        file.writelines(lines)  

update_env_file('DeviceMgmtAPI.env', 'GIT_VERSION', '1.3.44')
print("Update successfully in DeviceMgmtAPI.env")

update_env_file('DeviceMgmtWebApp.env', 'DOCKER_VERSION', '21.2.3')
print("Update successfully in DeviceMgmtWebApp.env")
