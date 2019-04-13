import datetime
from src.common.database import Database
import uuid


class Goal(object):

    def __init__(self, userid, title, content, created_date=datetime.datetime.utcnow(), _id=None):
        self.userid=userid
        self.title = title
        self.content=content
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='goals', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'userid':self.userid,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, _id):
        goal_data = Database.find_one(collection='goals', query={'_id' : _id})
        return cls(**goal_data)

    @staticmethod
    def from_user(id):
        return [goal for goal in Database.find(collection='goals', query={'userid': id})]
