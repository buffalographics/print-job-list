import os
import glob
import json


def search_dirs(root_dir):
    if os.path.exists(root_dir) is False:
        print("Directory doesnt exist")
    else:
        obj = {}
        root_dirs = os.listdir(root_dir)
        for dir in root_dirs:
            current_dir = os.path.join(root_dir, dir)
            if os.path.isdir(current_dir):
                if 'PRINT' in os.listdir(current_dir):
                    obj[dir] = os.listdir(os.path.join(current_dir, 'PRINT'))
            else:
                obj[dir] = search_dirs(current_dir)
        return obj


path = "/Volumes/GoogleDrive/Shared drives/Buffalo Graphics/clients"
clients_obj = search_dirs(path)


print(json.dumps(clients_obj, indent=4, sort_keys=True))
pretty_print(glob.glob(path+'/**/*/PRINT', recursive=True))
print()
