import os
from abc import ABC, abstractmethod
from pymongo import MongoClient
import certifi


def post_history_price():
    
    
    
    data = get_last_minutes_price()
    timestamp = data['timestamp']
    existing_entry = collection.find_one({'timestamp': timestamp})

    if existing_entry is None:
        collection.insert_one(data)
    client.close()
    return data['close_price']



class MongoDBMixin(ABC):
    def __init__(self):
        self.mongo_uri = os.getenv('MONGO_URI')

    def connect(self, db_name, collection_name):
        self.client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        db = self.client[db_name]
        collection = db[collection_name]
        return collection
    
    def disconnect(self):
        self.client.close()
    
    @abstractmethod
    def insert_new(self):
        pass 

    @abstractmethod
    def update(self):
        pass
        