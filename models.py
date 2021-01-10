from datetime import timedelta

from flask_jwt_extended import create_access_token
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash

Base = declarative_base()


class Show(Base):
    __tablename__ = "show"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    show_type = Column(String)
    description = Column(String)
    time = Column(String)
    place = Column(String)

    def __init__(self, name, show_type, description, time, place):
        self.name = name
        self.show_type = show_type
        self.description = description
        self.time = time
        self.place = place


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    password = Column(String)
    phone = Column(String)
    mail = Column(String, unique=True)
    admin = Column(Integer)

    def __init__(self, name, password, phone, mail, admin):
        self.phone = phone
        self.name = name
        self.mail = mail
        self.password = password
        self.admin = admin

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, mail, password):
        from app import session
        user = session.query(cls).filter(cls.mail == mail).one()
        if not check_password_hash(user.password, password):
            raise Exception('No user with this password')
        return user


class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, unique=True)
    is_avaliable = Column(Integer)
    clas = Column(String)
    show_ = Column(Integer, ForeignKey(Show.id))
    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, is_avaliable, clas, show_, user_id):
        self.is_avaliable = is_avaliable
        self.clas = clas
        self.show_ = show_
        self.user_id = user_id
