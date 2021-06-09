# %%
import os

from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
from progress.bar import Bar

client = MongoClient(host='localhost', port=27017)
db = client['buffalographics']

dir = "/Volumes/GoogleDrive/Shared drives/Buffalo Graphics/clients"
print(os.listdir(dir))


def sync_clients() -> None:

    if os.path.isdir(dir) is False:
        print(f"{dir}\nis not a directory")
        return

    folder_clients = os.listdir(dir)
    new_clients = []

    for client_name in folder_clients:
        client = db.clients.find_one({'name': client_name})
        if client is None:
            new_clients.append(client_name)

    if len(new_clients) > 0:

        for client_name in new_clients:

            try:
                db.clients.insert_one({
                    "name":
                    client_name,
                    "dir_path":
                    os.path.join(dir, client_name),
                })

                print(client_name)

            except DuplicateKeyError as e:
                print(e)

    else:
        print("Clients are up to date")


sync_clients()
