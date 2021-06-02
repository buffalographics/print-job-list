from connect import Client

db = Client()

# c_count = db["clients"].delete_many({}).deleted_count
# print(f"deleted {c_count} clients")
p_count = db["projects"].delete_many({}).deleted_count
print(f"deleted {p_count} projects")
f_count = db["files"].delete_many({}).deleted_count
print(f"deleted {f_count} files")
