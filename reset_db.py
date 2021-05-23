# %%
from connect import Client

db = Client()
# %% Reset clients

db["clients"].delete_many({})

# %% Reset projects

db["projects"].delete_many({})

# %% Reset files
db["files"].delete_many({})
