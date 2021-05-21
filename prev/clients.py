import os
import uuid
import json
from utils import pretty_print
path = "/Volumes/GoogleDrive/Shared drives/Buffalo Graphics/clients"
with open('data.txt') as json_file:

    data = json.load('data.json')

print(data)


clients = []

for name in os.listdir(path):
    client = {
        'id': str(uuid.uuid4()),
        'name': name
    }
    clients.insert(0, client)

print(clients)

data = {
    'clients': clients
}


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
