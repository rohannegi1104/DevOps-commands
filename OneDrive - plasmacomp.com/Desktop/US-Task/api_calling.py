#How to call api from python

import requests

url = 'https://api.postalpincode.in/pincode/249294'  # API URL for the postal pincode lookup
response = requests.get(url)

# Print the response code and content
print(f"The response code for this API request is: {response.status_code}")
