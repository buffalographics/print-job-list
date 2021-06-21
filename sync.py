# %%
import os
from glob import glob

from dotenv import load_dotenv
from progress.bar import Bar
from pymongo import MongoClient

from file_props import file_props

load_dotenv('./.env.local')

dir = os.getenv('CLIENTS_DIR_PATH')
tbn_dir = os.getenv('TBN_DIR')
mongo_uri = os.getenv('MONGO_URI')

print_files = glob(f"{dir}/**/PRINT/*.pdf", recursive=True)
bar = Bar('Syncing Files', max=len(print_files))

clients = {}
projects = {}
files = []
existing_clients = []
existing_projects = []
existing_files = []

db = MongoClient(mongo_uri)[os.getenv('DB_NAME')]

try:
    for ec in db.clients.find():
        existing_clients.append(ec['name'])
except Exception as err:
    print(err)

try:
    for ep in db.projects.find():
        existing_projects.append(ep['directory'])
except Exception as err:
    print(err)

try:
    for ef in db.files.find():
        existing_files.append(ef['path'])
except Exception as err:
    print(err)


for full_file_path in print_files:
    file_path = full_file_path.removeprefix(f"{dir}/")
    [project_dir, file_name] = file_path.removesuffix('.pdf').rsplit('/', 1)
    [client_name, info] = file_path.split('/', 1)
    project_name = project_dir.removeprefix(f"{client_name}/").rsplit('/',
                                                                      1)[0]

    if client_name not in existing_clients and clients.get(
            client_name) is None:
        clients[client_name] = {
            'name': client_name,
            'directory': os.path.join(dir, client_name)
        }

    if project_dir not in existing_projects and projects.get(
            project_dir) is None:
        projects[project_dir] = {
            'name': project_name,
            'client': client_name,
            'directory': project_dir,
        }

    if file_path not in existing_files:
        files.append(
            file_props(full_file_path, file_path, file_name, client_name,
                       project_dir))

    bar.next()

bar.finish()

# Insert unsynced clients
if len(clients.keys()) > 0:
    try:
        db.clients.insert_many(clients.values())
    except Exception as err:
        print(err)

# insert unsynced projects
if (len(projects.keys())) > 0:
    try:
        db.projects.insert_many(projects.values())
    except Exception as err:
        print(err)

# insert unsynced files
if len(files) > 0:
    try:
        db.files.insert_many(files)
    except Exception as err:
        print(err)
