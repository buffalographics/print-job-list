import os
import fitz
from dotenv.main import load_dotenv
from progress.bar import FillingSquaresBar
from pymongo import MongoClient

load_dotenv('.env.local')

dir = os.getenv('CLIENTS_DIR_PATH')
tbn_dir = os.getenv('TBN_DIR')
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.buffalographics


def tbn_from_pdf(obj_path, ext='.jpg', cache_dirname='tbn'):
    pdf_path = os.path.join(dir, obj_path)
    tbn = obj_path.replace(' ', '_').replace('/', '-').replace('.pdf',
                                                               ext).lower()
    cache_path = os.path.join(
        os.getcwd(),
        '__pycache__',
        cache_dirname,
    )

    if os.path.isdir(cache_path) is False:
        os.mkdir(cache_path)

    cache_file = os.path.join(cache_path, tbn).lower()

    if os.path.isfile(cache_file) is False:
        doc = fitz.open(pdf_path)
        page = doc.loadPage(0)  # number of page
        pix = page.getPixmap()
        pix.writePNG(cache_file)

    return tbn


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
