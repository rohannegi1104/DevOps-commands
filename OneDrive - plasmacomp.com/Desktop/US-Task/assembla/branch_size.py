import subprocess
import os

# Your Assembla API credentials and Git credentials
API_KEY = "b3e2b2e478634a951707"
API_SECRET = "fa4a28e7c094e4542ea4041961a779813ccd218a"
ASSEMBLA_URL = "https://api.assembla.com/v1/spaces.json"
headers = {
    "X-Api-Key": API_KEY,
    "X-Api-Secret": API_SECRET
}

def get_branch_size(branch_name: str):
    """Returns the size of the repository when checked out at a specific branch."""
    try:
        # Checkout to the branch
        checkout_command = ["git", "checkout", branch_name]
        subprocess.run(checkout_command, check=True)

        # Get the size of the repository using 'du' (disk usage)
        du_command = ["du", "-sh", "."]  # Get the size of the current directory (repository)
        size_output = subprocess.check_output(du_command, text=True).strip().split()[0]
        
        return size_output
    except subprocess.CalledProcessError as e:
        print(f"Error getting size for branch '{branch_name}': {e}")
        return None

def clone_and_list_branches(git_url: str):
    
    # Get the repo name from the Git URL
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
            return

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
        total_branches = sum(bool(branch.strip()) for branch in branches)
        print(f"\nTotal number of remote branches in the repository: {total_branches}")

        # List all branches with their sizes
        print("\nBranch sizes:")
        for branch in branches:
            branch_name = branch.strip()
            if branch_name:  # Ensure branch name is not empty
                branch_size = get_branch_size(branch_name)
                if branch_size:
                    print(f"- {branch_name}: {branch_size}")

    except subprocess.CalledProcessError as e:
        print(f"Error fetching branches: {e}")

# Example Usage
git_url = "https://git.assembla.com/Plasma-Portfolio/analyze.git"  # Git URL of the repository
clone_and_list_branches(git_url)
