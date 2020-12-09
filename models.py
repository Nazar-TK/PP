from sqlalchemy import Column,Integer,ForeignKey,String,DATE,create_engine
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:1234@localhost/db11", echo = True)
Session = orm.sessionmaker(bind=engine)
Base = declarative_base()

class show(Base):
    __tablename__ = "show"
    name = Column(String(25))
    show_id = Column(Integer, primary_key=True)
    show_type = Column(String)
    description = Column(String)
    time = Column(DATE)
    place = Column(String(1000))

class users(Base):
    __tablename__ = "users"
    name = Column(String(20))
    phone = Column(String(20))
    mail = Column(String(20))
    id = Column(Integer, primary_key=True)

class ticket(Base):
    __tablename__ = "ticket"
    code = Column(Integer, primary_key=True)
    is_avaliable = Column(String(20))
    clas = Column(String(20))
    show_ = Column(Integer, ForeignKey(show.show_id))
    show1 = orm.relationship(show)
    user_id = Column(Integer, ForeignKey(users.id))
    user = orm.relationship(users)
