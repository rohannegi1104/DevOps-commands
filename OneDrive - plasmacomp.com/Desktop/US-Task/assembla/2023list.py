import requests
import subprocess
import os

API_KEY = "b3e2b2e478634a951707"
API_SECRET = "fa4a28e7c094e4542ea4041961a779813ccd218a"
ASSEMBLA_URL = "https://api.assembla.com/v1/spaces.json"
headers = {
    "X-Api-Key": API_KEY,
    "X-Api-Secret": API_SECRET
}

git_url = "https://git.assembla.com/Plasma-Portfolio/c2m-ci.C2M.git" 
# username = "rohan_n"  
# token = "7765605f85d06a987cd42ac5786bf80f8f031607"  

response = requests.get(ASSEMBLA_URL, headers=headers)

if response.status_code == 200:
    print("Connection to Assembla successful!")
else:
    print(f"Error connecting to Assembla: {response.status_code}, {response.text}")
    exit()

# Determine the repository name from the URL
repo_name = git_url.split("/")[-1].replace(".git", "")

# Check if the repository already exists locally
if os.path.isdir(repo_name):
    print(f"The repository '{repo_name}' already exists locally. Skipping clone.")
else:
    try:
        # If the repository doesn't exist, clone it
        clone_command = [
            "git", "clone", git_url
        ]
        subprocess.run(clone_command, check=True)
        print("Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        exit()

# Change to the cloned repository's directory
os.chdir(repo_name)

try:
    # Fetch all remote branches
    fetch_command = ["git", "fetch", "--all"]
    subprocess.run(fetch_command, check=True)

    # List all branches (local and remote)
    branches_command = ["git", "branch", "-a"]
    branches = subprocess.check_output(branches_command, text=True).splitlines()

    # Print out all branches, including master and remote ones
    print("All branches in the repository:")
    for branch in branches:
        print(branch.strip())  # Print each branch name

    # Calculate the total number of branches
    total_branches = len([branch for branch in branches if branch.strip()])  # Count non-empty branches
    print(f"\nTotal number of branches in the repository: {total_branches}")

except subprocess.CalledProcessError as e:
    print(f"Error fetching branches: {e}")