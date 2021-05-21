#%%
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import os

load_dotenv()


def Client():
    env_keys = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"]

    conf = {}

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    for key in env_keys:
        val = os.getenv(key)
        print(val)
        if val is None:
            print(f"Missing env variable {key}")
    mongo_uri = f"mongodb+srv://{DB_USER}:" + DB_PASSWORD + f"@{DB_HOST}"
    client = MongoClient(mongo_uri)
    db = client.buffalographics

    return db
