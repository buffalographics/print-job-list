from connect import Client
import os

from pymongo.errors import DuplicateKeyError

from config import Config

db = Client()
clients_dir_path = Config().clients_dir_path


def sync_clients(dir: str) -> None:

    if os.path.isdir(dir) is False:
        print(f"{dir}\nis not a directory")
        return

    folder_clients = os.listdir(clients_dir_path)
    new_clients = []

    os.listdir(dir)

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
                    "file_path":
                    os.path.join(dir, client_name),
                })

                print(client_name)

            except DuplicateKeyError as e:
                print(e)

    else:
        print("Clients are up to date")
