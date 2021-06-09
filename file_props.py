from util import file_size, pdf_dim


def file_props(full_file_path: str, local_file_path: str, name: str,
               client_name: str, directory: str):
    """creates an obj with all properties for a print file

    Args:
        full_file_path (str): [description]
        local_file_path (str): [description]
        name (str): [description]
        client_name (str): [description]
        directory (str): [description]

    Returns:
        [type]: [description]
    """

    qty = None

    file_obj = {
        "name": name,
        "client": client_name,
        "directory": directory,
        'path': local_file_path,
        "size": file_size(full_file_path),
        'dimensions': pdf_dim(full_file_path),
        'qty': qty,
    }

    if file_obj['dimensions'] is None:
        file_obj['error'] = True

    try:
        file_obj['qty'] = int(name.lower().rsplit('qty_', 1).pop())

    except Exception as err:
        print(err)

    return file_obj
