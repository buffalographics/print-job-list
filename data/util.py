import os
from pdfrw import PdfReader
import json


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


def create_file_obj(file):
    sizes = pdf_dim(file)

    file_obj = {
        'full_path': file,
        'file_name': file.split('/').pop(),
        'width': sizes['width'],
        'height': sizes['height'],
        'size': file_size(file),
        'qty': ''
    }

    return file_obj
