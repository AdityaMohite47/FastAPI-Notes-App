import os
from pymongo import MongoClient
import dotenv

dotenv.load_dotenv()

def get_mongodb_connection():
    username = os.getenv('MONGO_USERNAME')
    password = os.getenv('MONGO_PASSWORD')
    host = os.getenv('MONGO_HOST', 'localhost')
    port = os.getenv('MONGO_PORT', 27017)
    auth_source = os.getenv('MONGO_AUTH_SOURCE', 'admin')
    auth_mechanism = os.getenv('MONGO_AUTH_MECHANISM', 'SCRAM-SHA-256')
    db_name = os.getenv('MONGO_DATABASE')
    
    if not db_name:
        raise ValueError("MONGO_DATABASE environment variable is not set.")

    if username and password:
        uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}&authMechanism={auth_mechanism}"
    else:
        uri = f"mongodb://{host}:{port}/"
    
    client = MongoClient(uri)
    return client[db_name]