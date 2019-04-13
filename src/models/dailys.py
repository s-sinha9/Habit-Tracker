import datetime
from src.common.database import Database
import uuid

from src.models.hours import Hour


class Daily(object):

    def __init__(self, userid, title=None, description=None, date=datetime.datetime.today(), _id=None):
        weekname = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.userid=userid
        self.title=weekname[date.weekday()] if title is None else title
        self.description="%d.%d.%d"%(date.day,date.month,date.year) if description is None else description
        self.created_date = date
        self._id=uuid.uuid4().hex if _id is None else _id

    def new_hour(self, start, end, content):
        hour=Hour(start=start,
                  end=end,
                  content=content,
                  date=self.description)
        hour.save_to_mongo()

    def get_hours(self):
        return Hour.from_daily(self.description)


    def save_to_mongo(self):
        Database.insert(collection='daily', data=self.json())

    def json(self):
        return {
            'userid':self.userid,
            'description': self.description,
            'date': self.created_date,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, _id):
        daily_data= Database.find_one(collection='daily', query={'_id':_id})
        return cls(**daily_data)

    @classmethod
    def find_by_user(cls, userid):
        daily = Database.find(collection='daily', query={'userid': userid})
        return [cls(**daily) for daily in daily]

    @classmethod
    def find_by_date(cls, description):
        daily=Database.find(collection='daily', query={'description': description})
        return [cls(**daily) for daily in daily]
