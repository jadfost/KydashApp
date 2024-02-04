# db.py
from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb+srv://jadfost:Dorothy1ove@cluster0.2ixoaaa.mongodb.net/?retryWrites=true&w=majority')
    db = client['kydash']
    return db

def get_users_collection():
    db = get_db()
    return db['usuarios']

def get_tradicional_collection():
    db = get_db()
    return db['tradicional']

def get_unique_years():
    db = get_db()
    years = db['tradicional'].distinct('AÑO')
    return sorted(years, reverse=True)

def get_unique_months():
    db = get_db()
    months = db['tradicional'].distinct('MES')
    return sorted(months)

def get_unique_medicion_channels():
    db = get_db()
    channels = db['tradicional'].distinct('CANAL MEDICIÓN')
    return sorted(channels)

def get_unique_medicion_executive():
    db = get_db()
    channels = db['tradicional'].distinct('EJECUTIVO')
    return sorted(channels)