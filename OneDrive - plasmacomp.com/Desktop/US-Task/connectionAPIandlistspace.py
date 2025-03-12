#connection with assembla and list of all space 

import requests

# API credentials
API_KEY = "b3e2b2e478634a951707"  # Replace with your actual API key
API_SECRET = "fa4a28e7c094e4542ea4041961a779813ccd218a"  # Replace with your actual API secret

# Base URL for Assembla API
assembla_url = "https://api.assembla.com"

# Headers for authentication
auth = {
    "X-Api-key": API_KEY,
    "X-Api-Secret": API_SECRET
}

# Step 1: Test connection to Assembla API (optional)
def test_connection():
    try:
        # Send a test request to verify the connection (Get user info)
        user_endpoint = "/v1/users/me.json"
        response = requests.get(assembla_url + user_endpoint, headers=auth)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Connection successful!")
            print("User Info:", response.json())  # You can see user info here to confirm connection
        else:
            print(f"Failed to connect to Assembla API. Status code: {response.status_code}")
            print("Error response:", response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

# Step 2: Fetch all spaces
def fetch_all_spaces():
    try:
        # Endpoint to fetch spaces
        spaces_endpoint = "/v1/spaces.json"
        
        # Make a GET request to the Assembla API to fetch spaces
        response = requests.get(assembla_url + spaces_endpoint, headers=auth)

        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully fetched spaces!")
            spaces = response.json()  # Convert the response to JSON
            if spaces:
                print("List of Spaces:")
                for space in spaces:
                    print(f"Space ID: {space['id']}, Name: {space['name']}")
            else:
                print("No spaces found.")
        else:
            print(f"Failed to fetch spaces. Status code: {response.status_code}")
            print("Error response:", response.text)
    except Exception as e:
        print(f"An error occurred while fetching spaces: {e}")

# Run the connection test first
test_connection()

# After confirming the connection, fetch all spaces
fetch_all_spaces()
