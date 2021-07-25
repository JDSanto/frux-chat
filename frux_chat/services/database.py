import os
import datetime
from pymongo import MongoClient

class Database:

    def __init__(self):
        self.client = MongoClient(os.environ['DATABASE_URL'])
        self.db = self.client[os.environ['DATABASE_NAME']]

    def get_user_collection(self):
        return self.db.users

    def insert_user(self, id, token):
        value = {
            'token': token
        }
        self.db.users.update(
           {'_id': id},
           value,
           upsert=True
        )
        return value

    def get_user(self, id):
        return self.db.users.find_one({'_id': id})


    def insert_notification(self, user_id, title, body):
        value = {
            'user_id': user_id,
            'title': title,
            'body': body,
            'created_at': datetime.datetime.now()
        }
        self.db.notifications.insert(value)
        return value


    def get_notifications(self, user_id):
        return list(self.db.notifications.find({'user_id': user_id}))


database = Database()
