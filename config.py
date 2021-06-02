from os import environ
from typing import TypedDict

from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')


class Config():
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    clients_dir_path: str
    db_uri: str
    db_user = environ.get("DB_USER")
    db_password = environ.get("DB_PASSWORD")
    db_host = environ.get("DB_HOST")
    db_name = environ.get("DB_NAME")
    clients_dir_path = environ.get("CLIENTS_DIR_PATH")
    db_uri = environ.get("DB_URI")
