import datetime
import uuid

from flask import session

from src.common.database import Database
from src.models.dailys import Daily
from src.models.goals import Goal


class User(object):
    def __init__(self, email, password, _id=None):
        self.email=email
        self.password=password
        self._id=uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email":email})
        if data is not None:
            return cls(**data)
    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password==password
        return False

    @classmethod
    def register(cls,email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user=cls(email, password)
            new_user.save_to_mongo()
            session['email']=email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email']=user_email

    @staticmethod
    def logout():
        session['email']=None


    def get_daily(self,id):
        return Daily.find_by_user(id)

    def new_daily(self):
        daily= Daily(userid=self._id,
                     date=datetime.datetime.utcnow())
        daily.save_to_mongo()

    def get_goal(self,id):
        return Goal.from_user(id)

    def new_goal(self, title, content, _id=None):
        goal= Goal(userid=self._id,
                   title=title,
                   content=content,
                   created_date=datetime.datetime.utcnow())
        goal.save_to_mongo()

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password":self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())