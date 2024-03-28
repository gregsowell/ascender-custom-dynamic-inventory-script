#!/usr/bin/env python
#test import script
import json

# Specify the path to the JSON payload file
json_payload_file = 'json-payload'

# Read the JSON payload from the file
with open(json_payload_file, 'r') as file:
    json_payload = file.read()

# Parse the JSON payload
inventory_data = json.loads(json_payload)

# Initialize inventory data structures
ansible_inventory = {
    '_meta': {
        'hostvars': {}
    },
    'all': {
        'hosts': [],
        'vars': {
            # You can define global variables here
        }
    }
}

# Initialize group dictionaries for each OS
os_groups = {}

# Process each host in the JSON payload
for host in inventory_data['hosts']:
    host_id = host['id']
    hostname = host['hostname']
    ip_address = host['ip_address']
    status = host['status']
    os = host['os']
    location = host['location']
    owner = host['owner']

    # Add the host to the 'all' group
    ansible_inventory['all']['hosts'].append(hostname)

    # Create host-specific variables
    host_vars = {
        'ansible_host': ip_address,
        'status': status,
        'os': os,
        'location': location,
        'owner': owner
        # Add more variables as needed
    }

    # Add the host variables to the '_meta' dictionary
    ansible_inventory['_meta']['hostvars'][hostname] = host_vars

    # Add the host to the corresponding OS group
    if os not in os_groups:
        os_groups[os] = {
            'hosts': []
        }
    os_groups[os]['hosts'].append(hostname)

# Add the OS groups to the inventory
ansible_inventory.update(os_groups)

# Print the inventory in JSON format
print(json.dumps(ansible_inventory, indent=4))
