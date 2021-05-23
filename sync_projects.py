# %%
from glob import glob

from get_config import get_config
from Mongo import Client


def link_jobs():
    db = Client()["clients"]
    clients_dir = get_config()["clients_dir_path"]
    job_paths = glob(clients_dir + "/**/**/*/PRINT", recursive=True)
    found = {}

    for job_path in job_paths:

        jobs = job_path.removeprefix(clients_dir + "/").split("/")
        name = jobs.pop(0)
        client = found.get(name, db.find_one({"name": name}))

        for job in reversed(jobs):
            obj = {"client": client}
            print(obj)


link_jobs()
