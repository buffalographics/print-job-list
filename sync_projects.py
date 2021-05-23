# %%
from glob import glob

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
        l = len(jobs)
        for o in range(l):
            job = {
                "client_id": client["_id"],
                "client_name": client.name,
                "name": jobs[o],
                "belongs_to": jobs[o - 1],
            }

            db["projects"].insert_one(job)


link_jobs()

# %%
