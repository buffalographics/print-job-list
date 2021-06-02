from time import time

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from operator import itemgetter

from config import Config

config = Config()
db_name = config.db_name
db_user = config.db_user
db_password = config.db_password
db_host = config.db_host
clients_dir_path = config.clients_dir_path


class Client():
    clients: Collection
    projects: Collection
    files: Collection

    def __init__(self):
        self.db_name = config.db_name
        self.db_user = config.db_user
        self.db_password = config.db_password
        self.db_host = config.db_host
        self.mongo_uri = (f"mongodb+srv://{db_user}:" + db_password +
                          f"@{db_host}")
        self.clients_dir_path = config.clients_dir_path
        try:
            start = time()
            # attempt to create a client instance of PyMongo driver
            client = MongoClient(self.mongo_uri)

            # call the server_info() to verify that client instance is valid
            client.server_info()  # will throw an exception

            db = client[db_name]
            dur = time() - start
            print(f"Connection Success: {dur}")
            self.collections = db.list_collection_names()
            self.clients = db.client.clients
            self.projects = db.client.projects
            self.files = db.client.files

        except ConnectionError as e:
            print("Connection error")
            print(e)

    def reset_col(self, col_name):
        try:
            client = MongoClient(self.mongo_uri)
            db = client[db_name]
            count = db[col_name].delete_many({}).deleted_count
            print(f"deleted {count} {col_name}")
        except Exception as err:
            print(err)
