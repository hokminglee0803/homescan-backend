
import certifi
from pymongo import MongoClient
import app.config

settings = app.config.get_settings()

client = MongoClient(settings.mongodb_connection_string, tlsCAFile=certifi.where())
database = client[settings.db_name]

def connect_to_mongodb():
    client.server_info()


def close_mongodb_connection():
    client.close()


def get_database():
    return database
