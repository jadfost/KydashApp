import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['kydash']
collection = db['usuarios']

def get_user(username):
    return collection.find_one({'username': username})

def create_user(username, password):
    if not get_user(username):
        collection.insert_one({'username': username, 'password': password})
        return True
    return False
