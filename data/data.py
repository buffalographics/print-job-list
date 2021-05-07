# %%
import json
import os
from glob import glob
from util import create_file_obj
# from pymongo import MongoClient
# user = "buffalographics"

# col = "buffalographics"
# uri = f"mongodb+srv\\[:]\\{user}\\//:Bgsince21@cluster0.z7wmc.mongodb.net/{col}"
# client = MongoClient(uri)

# db = client.buffalographics

# clients_collection = db.clients

clients_dir = "/Volumes/GoogleDrive/Shared drives/Buffalo Graphics/clients"
data_store = 'data.json'


def build_clients(dir):
    clients = {}
    if os.path.isfile(data_store):
        with open(data_store) as json_file:
            clients = json.load(json_file)['clients']
    else:
        with open(data_store, 'w') as outfile:
            json.dump({'clients': {}}, outfile)

    for client in os.listdir(dir):
        client_dir = os.path.join(dir, client)

        if client not in clients.keys() and os.path.isdir(client_dir):

            clients[client] = {'name': client}

    with open(data_store, 'w') as outfile:
        json.dump({'clients': clients}, outfile)

    print(clients)


build_clients(clients_dir)


def builder(dir):
    clients = {}
    with open(data_store) as outfile:
        clients = json.load(outfile)['clients']
    for client in clients.keys():
        jobs = {}

        client_dir = os.path.join(dir, client)
        default = glob(f"{client_dir}/PRINT/*.pdf", recursive=True)

        if len(default) > 0:
            files = {}
            for file in default:
                files[file.split('/').pop()] = create_file_obj(file)

            jobs['.'] = {'files': files}

        for job in glob(f"{client_dir}*/**/*/PRINT", recursive=True):
            job_full_path = job
            job = job.replace(dir+'/', '').replace('/PRINT', '')
            files = {}


            for file in glob(job_full_path+'/*.pdf'):
                file_obj = create_file_obj(file)

                # print(int(qty)
                files[file_obj['file_name']] = file_obj

            jobs[job] = {'full_path': job_full_path, 'files': files}

        clients[client] = {
            'full_path': dir,
            'jobs': jobs

        }

    with open(data_store, 'w') as outfile:
        json.dump({'clients': clients}, outfile)


print(builder(clients_dir))

# clients = builder(path)
# print(clients)

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
