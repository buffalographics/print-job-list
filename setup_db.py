import json
from collections import OrderedDict

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import CollectionInvalid

from config import Config


class SetupDb(MongoClient):
    db: Database

    def __init__(self, db_name):
        self.db_name = db_name
        try:
            config = Config()
            client = MongoClient(config["db_uri"])
            client.server_info()
            self.db = client[db_name]

        except ConnectionError as e:
            print(e)

    def create_collection(self, col_name, **kwargs):

        client = self.db

        client.create_collection(col_name)

validation = None
with open("db_schema.json") as f:
    validation = json.load(f)

config = Config()

db = MongoClient(config["db_uri"])['testing']

for collection in validation.keys():
    if collection not in db.list_collection_name():
        try:
            db.create_collection(collection)
        except Exception as e:
            print(e)
    try:
        query = [('collMod', collection),
                    ('validator', validation[collection])]

        command_result = db.command(OrderedDict(query))


    except CollectionInvalid as e:
        print(e)
