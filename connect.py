from time import time

from pymongo import MongoClient
from pymongo.database import Database

from operator import itemgetter

from config import Config

config = Config()

db_name = config.db_name
db_user = config.db_user
db_password = config.db_password
db_host = config.db_host


def Client() -> Database:

    mongo_uri = (f"mongodb+srv://{db_user}:" + db_password + f"@{db_host}")
    start = time()
    try:
        # attempt to create a client instance of PyMongo driver

        client = MongoClient(mongo_uri)

        # call the server_info() to verify that client instance is valid

        client.server_info()  # will throw an exception

        db = client[db_name]
        dur = time() - start
        print(f"Connection Success: {dur}")

        return db

    except ConnectionError as e:
        print("Connection error")
        print(e)
