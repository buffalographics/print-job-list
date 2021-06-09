# %% Connect
from time import time

from pymongo import MongoClient
from pymongo.database import Database

from config import Config

config = Config()

db_name = config.db_name
db_user = config.db_user
db_password = config.db_password
db_host = config.db_host
db_uri = config.db_uri


def Client() -> Database:

    start = time()
    try:
        # attempt to create a client instance of PyMongo driver

        # call the server_info() to verify that client instance is valid

        client = MongoClient(db_uri)

        client.server_info()  # will throw an exception

        db = client[db_name]
        dur = time() - start

        print(f"Connection Success: {round(dur)}")

        return db

    except ConnectionError as e:
        print("Connection error")
        print(e)


db = Client()
print(db.list_collection_names())
