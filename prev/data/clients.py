from pprint import pprint
import os
import pymongo
from pymongo import MongoClient
from glob import glob
from util import database

clients_dir = "/Volumes/GoogleDrive/Shared drives/Buffalo Graphics/clients"
db = database()
# %%


def clients_from_dir(dir):
    _clients = db["clients"]
    inserted = []

    for client in os.listdir(dir):

        if col.find_one({"name": client}) is None:

            client_obj = {
                "name": client,
                "file_path": os.path.join(clients_dir, client)
            }

            client_id = _clients.insert_one(client_obj).inserted_id

            if client_id is not None:
                inserted.append(
                    ({"_id": client_id, "name": client, }))

    pprint({
        "created": f"{len(inserted)} new clients",
        "client_count": _clients.count_documents({})
    })


clients_from_dir(clients_dir)
# %%


def format_job_name(job_full_path, dir_name):
    name = job_full_path.replace(dir_name+'/', '')
    if name == "PRINT":
        name = "default"
    name = name.replace("/PRINT", '')
    return name

# %%


def create_job_doc(obj, job_full_path):
    dir_name = os.path.join(clients_dir, obj['name'])

    job = {
        "client_id": obj["_id"],
        "name": format_job_name(job_full_path, dir_name),
        "files": []
    }

    return job
# %%


def link_jobs(q):
    _clients = db["clients"]
    _jobs = db["jobs"]

    client = col.find_one(q)
    dir_name = os.path.join(clients_dir, client['name'])

    jobs = []

    for job_full_path in glob(f"{dir_name}/**/**/PRINT", recursive=True):
        job = create_job_doc(client, job_full_path)
        jobs.append(_jobs.insert_one(job).inserted_id)

    _clients.update_one(q, {"$set": {'jobs': jobs}})


# %%
cs = col.find()
for c in cs:
    if 'name' in c:
        link_jobs({'name': c['name']})
