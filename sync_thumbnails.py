import os

from dotenv.main import load_dotenv
from progress.bar import FillingSquaresBar
from pymongo import MongoClient

from tbn_from_pdf import tbn_from_pdf

load_dotenv('.env.local')

dir = os.getenv('CLIENTS_DIR_PATH')
tbn_dir = os.getenv('TBN_DIR')
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.buffalographics


files = db.files.find({'tbn': {'$exists': False}})
updated = []
failed = []

bar = FillingSquaresBar('Syncing Thumbnails...',
                        max=db.files.count_documents(
                            {'tbn': {
                                '$exists': False
                            }}))

for file in files:
    bar.next()
    try:
        file['tbn'] = tbn_from_pdf(file['path'], ext='.jpg')
        updated.append({'_id': file['_id'], 'tbn': file['tbn']})
    except Exception as err:
        print(err)
        failed.append(file['path'])

bar.finish()

if len(updated) > 0:
    for changed in updated:

        try:
            db.files.find_one_and_update({'_id': changed['_id']},
                                         {'$set': {
                                             'tbn': changed['tbn']
                                         }})
        except Exception as err:
            print(err)
