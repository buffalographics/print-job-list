# %%
from config import Config
from glob import glob
from pprint import pprint
from pymongo.errors import WriteError
from connect import Client

db = Client()
clients_dir_path = Config().clients_dir_path


def sync_projects():
    project_paths = glob(clients_dir_path + "/**/**/*/PRINT", recursive=True)
    print(len(project_paths))
    cache = {}

    for project_path in project_paths:
        project_id = project_path.removeprefix(f"{clients_dir_path}/")
        [client_name, project_name] = project_id.split('/', 1)
        if db.projects.find_one({'project_id': project_id}) is not None:
            return
        client = cache.get(project_name,
                           db["clients"].find_one({"name": client_name}))

        if client_name not in cache.keys():
            cache[client_name] = client

        inserted_ids = []
        rejected_ids = []
        try:
            project = {
                "project_id": project_id,
                "client_id": client["_id"],
                "client_name": client_name,
                "name": project_name,
                "dir_path": project_path,
            }

            db.projects.insert_one(project).inserted_id

        except WriteError as e:
            rejected_ids.append(project_id)
            pprint(e._message)
