import requests
import subprocess
import os

# Assembla API credentials
API_KEY = "b3e2b2e478634a951707"
API_SECRET = "fa4a28e7c094e4542ea4041961a779813ccd218a"
ASSEMBLA_URL = "https://api.assembla.com/v1/spaces.json"
headers = {
    "X-Api-Key": API_KEY,
    "X-Api-Secret": API_SECRET
}

# Updated Git URL
git_url = "https://git.assembla.com/Plasma-Portfolio/analyze.git"  # Updated Git URL

# Check connection to Assembla
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
        clone_command = ["git", "clone", git_url]
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

    # List all remote branches
    branches_command = ["git", "branch", "-r"]  # Use -r for remote branches only
    branches = subprocess.check_output(branches_command, text=True).splitlines()

    # Calculate the total number of branches
    total_branches = len([branch for branch in branches if branch.strip() and branch.startswith("origin/")])  # Count non-empty remote branches
    print(f"Total number of remote branches in the repository: {total_branches}")

    # Optional: Check out each branch (if needed)
    for branch in branches:
        branch_name = branch.strip()
        if branch_name.startswith("origin/") and "HEAD" not in branch_name:
            local_branch_name = branch_name.replace("origin/", "")
            # Check for uncommitted changes
            status_command = ["git", "status", "--porcelain"]
            status_output = subprocess.check_output(status_command, text=True)
            if status_output:
                print(f"Cannot checkout '{local_branch_name}' due to uncommitted changes.")
                continue  # Skip to the next branch

            # Checkout the branch
            checkout_command = ["git", "checkout", local_branch_name]
            try:
                subprocess.run(checkout_command, check=True)
                print(f"Checked out branch: {local_branch_name}")
            except subprocess.CalledProcessError as e:
                print(f"Error checking out branch '{local_branch_name}': {e}")

except subprocess.CalledProcessError as e:
    print(f"Error fetching branches: {e}")