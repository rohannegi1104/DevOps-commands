import requests

# API setup
client_key = "b3e2b2e478634a951707"
client_secret = "fa4a28e7c094e4542ea4041961a779813ccd218a"
auth = {
    "X-Api-key": client_key,
    "X-Api-Secret": client_secret
}

# initial variables
project_spaces = ['Vibhor-test']
custom_tickets = ["RTno", "RCA", "CLCA"]

# Get user input 
milestone = int(input("Enter the milestone ID: "))
client_name_input = input("Enter the client name: ")

# Function to Fetch Data from Assembla API  
def fetch_data(project_space):
    try:
        assembla_url = f"https://api.assembla.com/v1/spaces/{project_space}/tickets.json"
        response = requests.get(assembla_url, headers=auth)
        if response.status_code == 200:
            return response.json()  
        else:
            print(f"Failed to fetch tickets: {response.status_code}")
            return []  
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return [] 

# Filter Tickets by Milestone and Client  
def receive_milestone_and_client(project_spaces, milestone, client_name):
    all_tickets = [] 
    for project_space in project_spaces:
        tickets = fetch_data(project_space)
        print(f"Fetched Tickets: {tickets}")
        for ticket in tickets:
            #checks if the ticket's milestone_id matches the given milestone and if the client_name matches the given client_name
            if ticket.get('milestone_id') == milestone and ticket.get('client_name') == client_name:
                all_tickets.append(ticket)
    return all_tickets

# Missing values check
def check_missing_values(ticket):
    missing_fields = []
    for ticket_field in custom_tickets:
         #it retrieves the value associated with the key ticket_field from the ticket dictionary
         #or
         #retrieves the single value for a given key in the ticket dictionary, not a list
        value = ticket.get(ticket_field)
        if value == "" or value == " " or value == ".":
            missing_fields.append(ticket_field)
    
    # Return a string message for missing fields or all filled
    if missing_fields:
        print(f"Ticket with ID {ticket['id']} is missing the following fields: {','.join(missing_fields)}")
                                         #joins the items in the missing_fields list into a single string
                 #','.join(missing_fields) combines the list of missing field names into a single string separated by commas
    else:
        print("All fields are filled.")

# Fetching the tickets
tickets_based_on_client_and_milestone = receive_milestone_and_client(project_spaces, milestone, client_name_input)
# Calls the function receive_milestone_and_client() to fetch tickets that match the provided milestone and client name.
# The result is stored in the variable tickets_based_on_client_and_milestone

# Display the results
if tickets_based_on_client_and_milestone:
    for ticket in tickets_based_on_client_and_milestone:
        ticket_field_status = check_missing_values(ticket)
        print(f"Ticket ID: {ticket['id']} - {ticket_field_status}")
else:
    print("No tickets match.")
