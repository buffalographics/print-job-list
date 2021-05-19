from pymongo import MongoClient
import os
from pdfrw import PdfReader
import json
import re


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        print(e)
        return False
    return True


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def pdf_dim(file):
    if os.path.isfile(file) and file.endswith('.pdf') and os.stat(file):
        sizes = {'height': '', 'width': ''}
        try:
            media_box = PdfReader(file).pages[0].MediaBox
            # [0, 0, height, width] in points

            h = (float(media_box[2]) / 72).__round__()
            w = (float(media_box[3]) / 72).__round__()

            sizes['height'] = f"{h}in"
            sizes['width'] = f"{w}in"

        except ValueError as e:
            print(e)
            print(f"Error getting dimensions of file\n{file}")

        return sizes


def qty_file_str(file):
    if 'qty' in file.lower():
        print(file)
        item = file.lower().replace('.pdf', '')
        item = item.split('qty').pop()
        return round(float(re.sub("[^0-9]", "", item)))
    else:
        return None


def create_file_obj(client_id, job_id, file):
    sizes = pdf_dim(file)
    file_name = file.split('/').pop()
    qty = qty_file_str(file_name)
    print(qty)
    file_obj = {
        "client_id": client_id,
        "job_id": job_id,
        'full_path': file,
        "width": sizes["width"],
        "height": sizes["height"],
        "size": file_size(file),
    }

    return file_obj


def database():
    user = 'buffalographics'
    pwd = "Bgsince21"
    host = "cluster0.z7wmc.mongodb.net"
    # col = "buffalographics"

    mongo_uri = f"mongodb+srv://{user}:" + \
        pwd + f"@{host}/"

    db = None

    start = time.time()

    try:

        # attempt to create a client instance of PyMongo driver

        client = MongoClient(mongo_uri)

    # call the server_info() to verify that client instance is valid

        client.server_info()  # will throw an exception

        print(time.time() - start)

        db = client["buffalographics"]

        return db

    except:

        print("connection error")

    # print the time that has elapsed

    print(time.time() - start)

    # %%
