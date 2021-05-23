from os import environ
from typing import TypedDict

from dotenv import load_dotenv


class ConfigDict(TypedDict):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    clients_dir_path: str


def Config() -> ConfigDict:
    load_dotenv()

    vals = (
        environ.get("DB_USER"),
        environ.get("DB_PASSWORD"),
        environ.get("DB_HOST"),
        environ.get("DB_NAME"),
        environ.get("CLIENTS_DIR_PATH"),
    )

    [db_user, db_password, db_host, db_name, clients_dir_path] = vals

    if all(isinstance(item, str) for item in vals):

        return {
            "db_user": db_user,
            "db_password": db_password,
            "db_host": db_host,
            "db_name": db_name,
            "clients_dir_path": clients_dir_path,
        }
