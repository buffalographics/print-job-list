import os
import glob
import utils

path = "/Volumes/GoogleDrive/Shared drives/Buffalo Graphics/clients"
paths = glob.glob(path+'/**/*/PRINT', recursive=True)


i = 0
for str in paths:
    paths[i] = str.replace(path+'/', '').replace('/PRINT', '')
    i = i+1
i = 0


def obj_maker(obj={}):
    i = 0
    for item in paths:
        obj[item] = item.split('/')
        i = i+1

    return obj


obj = obj_maker()

# for item in paths:
#     obj[item[0]] = item[0]

# def obj_tree_str()


utils.pretty_print(paths)
utils.pretty_print(obj)

# pretty_print(glob.glob(path+'/**/*/PRINT', recursive=True))
