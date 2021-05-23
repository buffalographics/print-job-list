from pymongo import MongoClient
from pymongo.database import Database

from config import Config


def Client() -> Database:
    config = Config()

    mongo_uri = (
        f"mongodb+srv://{config['db_user']}:"
        + config["db_password"]
        + f"@{config['db_host']}"
    )

    try:
        # attempt to create a client instance of PyMongo driver

        client = MongoClient(mongo_uri)

        # call the server_info() to verify that client instance is valid

        client.server_info()  # will throw an exception

        db = client[config["db_name"]]

        print("Connection Success")

        return db

    except ConnectionError as e:
        print("Connection error")
        print(e)


Client()
