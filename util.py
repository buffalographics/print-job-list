from collections.abc import Iterator, Iterable
import json
import os
import re

from pdfrw import PdfReader

from config import Config

config = Config()
clients_dir_path = config.clients_dir_path


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


units = [('INCHES', 72, 'in'), ('FEET', 864, 'ft'), ("YARD", 2592, 'yd'),
         ("CENTIMETER", 28.3465, 'cm')]


def make_unit_obj(amt, div):
    obj = {}
    obj['height'] = float(amt[0] / div)
    obj['width'] = float(amt[1] / div)
    obj['area'] = obj['height'] * obj['width']
    return obj


def pdf_dim(file):
    sizes = {}
    if os.path.isfile(file) and file.endswith('.pdf') and os.stat(file):

        for unit in units:
            name = unit[0]
            div = unit[1]

            try:
                media_box = PdfReader(file).pages[0].ArtBox
                print(media_box)
                # [0, 0, height, width] in points

                sizes[name.lower()] = make_unit_obj(
                    [float(media_box[2]),
                     float(media_box[3])], div)

            except ValueError as e:
                print(e)
                print(f"Error getting dimensions of file\n{file}")
                return None

    return sizes


def qty_file_str(file):
    if 'qty' in file.lower():
        print(file)
        item = file.lower().replace('.pdf', '')
        item = item.split('qty').pop()
        return round(float(re.sub("[^0-9]", "", item)))
    else:
        return None


def create_file_obj(client_id, project_id, file_obj):
    file = file_obj['file_path']
    sizes = None

    try:
        sizes = pdf_dim(file)
    except ValueError as e:
        print(e)

    file_name = file.split('/').pop()
    file_obj = {
        "client_id": client_id,
        "project_id": project_id,
        'client_name': file_obj['client_name'],
        "file_name": file_name,
        'full_path': file,
        "width": sizes["width"],
        "height": sizes["height"],
        "size": file_size(file),
    }

    return file_obj


def filep_vars(file_path):

    obj = {
        'file_name': None,
        'client_name': None,
        'project_name': None,
        'project_id': None,
        'file_id': None,
    }

    try:
        str_list = file_path.removeprefix(f"{config.clients_dir_path}/")
        str_list = str_list.split('/', 1)
        client_name = str_list[0]
        project_name = str_list[1].split('/', 1)[0]

        file_name = file_path.rsplit('/').pop()
        project_id = '/'.join([
            client_name,
            project_name,
            'PRINT',
        ])
        file_id = '/'.join([project_id, file_name])
        obj['file_name'] = file_name
        obj['client_name'] = client_name
        obj['project_name'] = project_name
        obj['project_id'] = project_id
        obj['file_id'] = file_id

    except Exception as err:
        print(err)
        return None

    return obj


def snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
