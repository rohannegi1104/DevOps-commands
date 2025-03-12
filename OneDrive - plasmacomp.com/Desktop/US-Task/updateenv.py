import os

repo_path = "/root/Assembla/Launchpad"
env_folder = os.path.join(repo_path, "ZerotoOne_Staging")

env_files = {
    "DeviceMgmtAPI.env": {"GIT_VERSION": "21.8.6"},
    "DeviceMgmtWebApp.env": {"GIT_VERSION": "13.8.5"},
}

if not os.path.exists(env_folder):
    print(f"Environment folder not found: {env_folder}. Exiting.")
    exit(1)

os.chdir(env_folder)

for file, updates in env_files.items():
    file_path = os.path.join(env_folder, file)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        keys_found = set()

        for line in lines:
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()

                if key in updates:
                    new_lines.append(f"{key}={updates[key]}\n")
                    keys_found.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        for key, value in updates.items():
            if key not in keys_found:
                new_lines.append(f"\n{key}={value}\n")

        with open(file_path, "w") as f:
            f.writelines(new_lines)

        print(f"Updated: {file}")
    else:
        print(f"File not found: {file}")
