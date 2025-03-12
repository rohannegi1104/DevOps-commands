import os
import subprocess as s

git_url = "https://git.assembla.com/Plasma-Portfolio/Launchpad.git"
env_folder_path = "Launchpad/ZerotoOne_Staging"  

def clone_repository():
    if not os.path.exists("Launchpad"):
        print("Cloning the repository...")
        s.run(["git", "clone", git_url])
    else:
        print("Repository already exists. ")

def update_env_file(env_file_path, key, value):
    lines = []
    key_exists = False

    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as file:
            for line in file:
                if line.startswith(f"{key}="):
                    line = f"{key}={value}\n"
                    key_exists = True
                lines.append(line)

    if not key_exists:
        lines.append(f"{key}={value}\n")

    with open(env_file_path, 'w') as file:
        file.writelines(lines)

# Main function execution
clone_repository()

update_env_file(os.path.join(env_folder_path, 'DeviceMgmtAPI.env'), 'S3__Password', 'abcdef')
print("Update successfully in DeviceMgmtAPI.env")

update_env_file(os.path.join(env_folder_path, 'DeviceMgmtWebApp.env'), 'DOCKER_VERSION', '46.78.8')
print("Update successfully in DeviceMgmtWebApp.env")