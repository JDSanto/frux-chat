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
        return list(self.db.notifications.find({'user_id': user_id}, {'_id': False}))


    def get_subscriptions_users(self, tag):
        subscriptions = self.db.subscriptions.find({'tag': tag})
        users = []
        for sub in subscriptions:
            user = self.db.users.find_one({"_id": sub['user_id']})
            if not user:
                continue
            users.append(user)
        return users


    def insert_subscription(self, tag, user_id):
        value = {
            'tag': tag,
            'user_id': user_id
        }
        self.db.subscriptions.update(
           {'_id': f'{tag}-{user_id}'},
           value,
           upsert=True
        )
        return value


    def remove_subscription(self, tag, user_id):
        key = f'{tag}-{user_id}'
        self.db.subscriptions.remove({'_id': key})
        return key


database = Database()
