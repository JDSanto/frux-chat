import datetime
import os

from pymongo import MongoClient


class Database:
    def __init__(self):
        self.client = MongoClient(os.environ['DATABASE_URL'])
        self.db = self.client[os.environ['DATABASE_NAME']]

    def get_user_collection(self):
        '''
        Return all users
        '''
        return self.db.users

    def insert_user(self, user_id, token):
        '''
        Inserts or updates a user
        '''
        value = {'token': token}
        self.db.users.update({'_id': user_id}, value, upsert=True)
        return value

    def get_user(self, user_id):
        return self.db.users.find_one({'_id': user_id})

    def insert_notification(
        self, user_id, title, body, project_id=None, chat_id=None, commenter_id=None
    ):
        '''
        Inserts a notification for the given user, with the current timestamp
        '''
        value = {
            'user_id': user_id,
            'title': title,
            'body': body,
            'project_id': project_id,
            'chat_id': chat_id,
            'commenter_id': commenter_id,
            'created_at': datetime.datetime.now(),
        }
        self.db.notifications.insert(value)
        return value

    def get_notifications(self, user_id):
        '''
        Returns all notifications for a given user
        '''
        return list(self.db.notifications.find({'user_id': user_id}, {'_id': False}))

    def get_chat(self, project_id):
        '''
        Returns all the messages for a given project
        '''
        return list(
            self.db.notifications.find(
                {'project_id': project_id, 'chat_id': {"$ne": None}}, {'_id': False}
            )
        )

    def get_subscriptions_users(self, tag):
        '''
        Returns all users that are subscribed to a given tag
        '''
        subscriptions = self.db.subscriptions.find({'tag': tag})
        users = []
        for sub in subscriptions:
            user = self.db.users.find_one({"_id": sub['user_id']})
            if not user:
                continue
            users.append(user)
        return users

    def insert_subscription(self, tag, user_id):
        '''
        Inserts a new subscription for a given user and tag
        '''
        value = {'tag': tag, 'user_id': user_id}
        self.db.subscriptions.update({'_id': f'{tag}-{user_id}'}, value, upsert=True)
        return value

    def remove_subscription(self, tag, user_id):
        '''
        Removes a subscription for a given user and tag
        '''
        key = f'{tag}-{user_id}'
        self.db.subscriptions.remove({'_id': key})
        return key


database = Database()
