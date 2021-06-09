# %%
from glob import glob
from pprint import pprint

from pymongo import MongoClient
from util import create_file_obj, filep_vars

from config import Config
from connect import Client
from progress.bar import Bar

client = MongoClient(host='localhost', port=27017)
db = client['buffalographics']

config = Config()
_clients = {}
_projects = {}
file_paths = glob(f"{config.clients_dir_path}/*/**/PRINT/*.pdf",
                  recursive=True)
bar = Bar('Processing', max=len(file_paths))
failed = []

for file_path in file_paths:
    args = {}
    for key, val in filep_vars(file_path).items():
        args[key] = val

    client_name = args.get('client_name')

    client = _clients.get(client_name)

    # try:

    if client is None:
        _clients[client_name] = db.clients.find_one({"name": client_name})

        client = _clients.get(client_name)

    project_id = args.get('project_id')
    project = _projects.get(project_id)

    if project is None:
        _projects[project_id] = db.projects.find_one(
            {"project_id": project_id})
        project = _projects.get(project_id)

    try:
        file_obj = create_file_obj(client.get("_id"), project_id, {
            'file_path': file_path,
            'client_name': client_name
        })
        if db.files.find_one(file_obj) is None:
            db.files.insert_one(file_obj)
    except Exception as err:
        print(err)

    bar.next()
print(failed)
bar.finish()
# pprint(file_paths)
