import os
dirs = os.listdir(path())
print(dirs)

obj = {}
for dir in dirs:
    i = 0
    folder = os.path.join(path, dir)
    jobs = glob.glob(folder+'/**/*/PRINT/*', recursive=True)
    print('jobs: ', jobs)
    # for job in jobs:
    conf = {
        'full_path': os.path.join(path, dir),
    }


for key, val in obj.items():
    list = obj[key]
    print(list)
    # obj[key].jobs = list
# pretty_print(obj)
