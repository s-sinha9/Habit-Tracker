import datetime
from src.common.database import Database
import uuid


class Hour(object):

    def __init__(self, dailyid, start, end, content, date=datetime.datetime.utcnow(), _id=None):
        self.dailyid=dailyid
        self.title = start+"-"+end
        self.content=content
        self.created_date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='hour', data=self.json())

    def json(self):
        return {
            'daily_id':self.dailyid,
            'title': self.title,
            'content': self.content,
            'created_date': self.created_date,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        hour_data= Database.find_one(collection='hour', query={'_id' : _id})
        return cls(**hour_data)

    @staticmethod
    def from_daily(dailyid):
        return [hour for hour in Database.find(collection='hour', query={'daily_id': dailyid})]
