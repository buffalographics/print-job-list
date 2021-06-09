# %%

from enum import unique
import os
from typing import OrderedDict
from dotenv.main import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid

MongoClient().drop_database('buffalographics')
# %%

from enum import unique
from typing import OrderedDict
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid

load_dotenv('./.env.local')
client = MongoClient(os.environ.get('MONGO_URI'))
db = client['buffalographics']

collections = ['clients', 'projects', 'files']
schemas = {
    'clients':
    OrderedDict({
        'collMod': 'clients',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'properties': {
                    'name': {
                        'bsonType': 'string',
                        'description': 'Company Name'
                    },
                    'directory': {
                        'bsonType': 'string',
                        'description': 'Path to client folder'
                    }
                },
                'required': ['name', 'directory']
            }
        }
    }),
    'projects':
    OrderedDict({
        'collMod': 'projects',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'properties': {
                    'name': {
                        'bsonType': 'string',
                        'description': 'Project Name'
                    },
                    'client': {
                        'bsonType': 'string',
                        'description': 'Company Name'
                    },
                    'directory': {
                        'bsonType': 'string',
                        'description': 'Path to project folder'
                    }
                },
                'required': ['name', 'client', 'directory']
            }
        }
    })
}

for col in collections:

    try:
        db.create_collection(col)
        if schemas.get(col) is not None:
            db.command(schemas[col])

    except CollectionInvalid as err:
        print(err)

db.clients.create_index([
    ('name', ASCENDING),
], unique=True)

db.projects.create_index([('name', ASCENDING), ('client', ASCENDING)],
                         unique=True)
db.files.create_index([('name', ASCENDING), ('project', ASCENDING),
                       ('client', ASCENDING)],
                      unique=True)

db.list_collection_names()
