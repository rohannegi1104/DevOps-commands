import requests

url = "https://api.postalpincode.in/pincode/249294"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Assumes the response is in JSON format
    print(data)  # This will print the actual JSON data
else:
    print(f"Error: {response.status_code}")

print("API call is successful through Python")
