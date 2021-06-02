# %%
from sync_clients import sync_clients
from sync_projects import sync_projects
from config import Config
from time import time

config = Config()

try:
    start = time()
    sync_clients(config.clients_dir_path)
    print(start - time())
except Exception as err:
    print(err)

# %%

try:
    start = time()
    sync_projects()
    print(start - time())
except Exception as err:
    print(err)
