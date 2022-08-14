import sqlalchemy as alc
import sqlalchemy.orm as alc_orm

import time

import models

# час, 5 часов, 5 дней, 25 дней, 4 месяца
INTERVALS = [
    60 * 60,
    60 * 60 * 5,
    60 * 60 * 24 * 5,
    60 * 60 * 24 * 25,
    60 * 60 * 24 * 30 * 4,
]

engine = alc.create_engine('sqlite:///bot_db')
session = alc_orm.sessionmaker(bind=engine)
s = session()


def add_word(user_id: int, word: str, translation: str) -> None:
    remember_time = round(time.time()) + INTERVALS[0]

    word = models.Word(
        user_id=user_id,
        word=word,
        translation=translation,
        update_time=remember_time,
    )
    s.add(word)
    s.commit()
