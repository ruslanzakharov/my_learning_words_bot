from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    SmallInteger,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bot_db')

Base = declarative_base()


class Word(Base):
    __tablename__ = 'Words'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    status = Column(SmallInteger, default=0)
    update_time = Column(Integer)


Base.metadata.create_all(engine)
