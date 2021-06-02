# %%
from glob import glob
from pprint import pprint

from pymongo.errors import WriteError
from config import Config
from connect import Client

db = Client()


def link_jobs():
    config = Config()
    clients_dir = config["clients_dir_path"]
    job_paths = glob(clients_dir + "/**/**/*/PRINT", recursive=True)
    found = {}

    for job_path in job_paths:

        jobs = job_path.removeprefix(clients_dir + "/").split("/")
        name = jobs.pop(0)
        client = found.get(name, db["clients"].find_one({"name": name}))
        print(client)
        l = len(jobs)
        for o in range(l):

            try:
                job = {
                    "client_id": client["_id"],
                    "client_name": client['name'],
                    "name": jobs[o],
                    "dir_path": job_path
                }

                db.projects.insert_one(job)

            except WriteError as e:

                pprint(e)


link_jobs()
'''

def sync_projects():
    job_paths = []
    cache = {'test Val': 'test'}
    for jobp in glob(clients_dir_path + "/**/**/*/PRINT", recursive=True):
        job_id = jobp.removeprefix(f"{clients_dir_path}/")
        [client_name, job_name] = job_id.split('/', 1)

        client = db.clients.find_one({'name': client_name})
        if cache.get(client_name, None) is None and client.get(
                client_name, None) is not None:
            cache[client_name] = client

        print(cache)
        job = db.projects.find_one({
            'client_id': cache[client_name]['_id'],
            'name': job_name
        })
        print(job)
        # if job is None:
        #     inserted_id = db.projects.insert_one({
        #         'job_id': job_id,
        #         'name': job_name
        #     }).inserted_id
        #     print(inserted_id)

    print(job_paths)
'''

# %%
