import os
import fitz


def tbn_from_pdf(obj_path, ext='.jpg', cache_dirname='tbn'):
    """creates a png thumbnail from pdf file path if one doesn't exist

    Args:
        obj_path ([type]): [description]
        ext (str, optional): [description]. Defaults to '.jpg'.
        cache_dirname (str, optional): [description]. Defaults to 'tbn'.

    Returns:
        [type]: [description]
    """
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
