from connect import Client
import os

from pymongo.errors import DuplicateKeyError

from config import Config


def sync_clients(dir: str) -> None:
    # return early on invalid paths

    if os.path.isdir(dir) is False:
        print(f"{dir}\nis not a directory")
        return

    folder_clients = os.listdir(dir)
    db = Client().client

    for folder_name in folder_clients:

        try:
            db.insert_one(
                {
                    "name": folder_name,
                    "file_path": os.path.join(dir, folder_name),
                    "projects": [],
                }
            )

        except DuplicateKeyError as e:
            return


sync_clients(Config()["clients_dir_path"])
