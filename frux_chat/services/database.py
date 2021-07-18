import os
from pymongo import MongoClient

class Database:

    def __init__(self):
        self.client = MongoClient(os.environ['DATABASE_URL'])
        self.db = self.client[os.environ['DATABASE_NAME']]

    def get_user_collection(self):
        return self.db.users

    def insert_user(self, id, token):
        return self.db.users.insert_one({
            '_id': id,
            'token': token
        })

    def get_user(self, id):
        return self.db.users.find_one({'_id': id})


database = Database()
