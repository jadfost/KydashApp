# db.py
from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb+srv://jadfost:Dorothy1ove@cluster0.2ixoaaa.mongodb.net/?retryWrites=true&w=majority')
    db = client['kydash']
    return db

def get_users_collection():
    db = get_db()
    return db['usuarios']