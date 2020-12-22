from sqlalchemy import Column, Integer, String, Boolean, orm, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Show(Base):
    __tablename__ = "show"
    show_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(25))
    show_type = Column(String)
    description = Column(String)
    time = Column(String)
    place = Column(String(1000))

    def __init__(self, name, show_type, description,time, place):
        self.name = name
        self.show_type = show_type
        self.description = description
        self.time = time
        self.place = place


class User(Base):
    __tablename__ = "users"
    name = Column(String(20))
    password = Column(String(100))
    phone = Column(String(20))
    mail = Column(String(30), unique=True)
    id = Column(Integer, primary_key=True, unique=True)

    def __init__(self, name, password, phone, mail):
        self.phone = phone
        self.name = name
        self.mail = mail
        self.password = password


class Ticket(Base):
    __tablename__ = "ticket"
    code = Column(Integer, primary_key=True, unique=True)
    is_avaliable = Column(Integer)
    clas = Column(String(20))
    show_ = Column(Integer, ForeignKey(Show.show_id))
    #show1 = orm.relationship(Show)
    user_id = Column(Integer, ForeignKey(User.id))
    #user = orm.relationship(User)

    def __init__(self, is_avaliable, clas, show_, user_id):
        self.is_avaliable = is_avaliable
        self.clas = clas
        self.show_ = show_
        self.user_id = user_id
