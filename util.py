import os
import re
from typing import Union

from pdfrw import PdfReader


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


def make_unit_obj(amt: Union[float, float], div: int / float):
    """returns an object containing
        - height
        - width
        - area

    Args:
        amt (Union[float, float]): [h in 'points', width in 'points']
        div ([type]): [number to divide by for your conversion]

    Returns:
        dict[str, float]: [description]
    """
    [h_pts, w_pts] = amt

    h = float(h_pts / div)
    w = float(w_pts / div)
    a = h * w

    unit = {
        'height': h,
        'width': w,
        'area': a
    }

    return unit


def pdf_dim(file):
    """[summary]

    Args:
        file ([type]): [description]

    Returns:
        [type]: [description]
    """
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
