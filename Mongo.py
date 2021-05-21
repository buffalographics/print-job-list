# %%
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
from pymongo.database import Database
from pymongo import MongoClient
import os
from pprint import pprint

load_dotenv()


def get_config() -> dict:
    env_keys = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"]
    missing_keys = []
    config = {}

    for key in env_keys:
        if not key in os.environ.keys():
            missing_keys.append(key)
        else:
            config[key] = os.environ.get(key)

    if len(missing_keys) > 0:
        print("Missing keys")
        pprint(missing_keys)
        return

    return config


def Client() -> Database:
    config = get_config()
    mongo_uri = f"mongodb+srv://{config['DB_USER']}:" + \
        config['DB_PASSWORD'] + f"@{config['DB_HOST']}"

    client = MongoClient(mongo_uri)

    db = client.buffalographics

    return db
