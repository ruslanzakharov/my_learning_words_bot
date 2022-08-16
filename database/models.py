from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    SmallInteger,
    create_engine,
    Boolean
)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bot_db')

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    # True если бот отправил слово и ждет перевода
    is_waiting = Column(Boolean, default=False)


class Word(Base):
    __tablename__ = 'Words'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id', ondelete='CASCADE'))
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    status = Column(SmallInteger, default=0)
    remember_time = Column(Integer)


Base.metadata.create_all(engine)
