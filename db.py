import sqlalchemy as alc
import sqlalchemy.orm as alc_orm

import time

from models import Word, User

# час, 5 часов, 5 дней, 25 дней, 4 месяца
INTERVALS = [
    60 * 60,
    60 * 60 * 5,
    60 * 60 * 24 * 5,
    60 * 60 * 24 * 25,
    60 * 60 * 24 * 30 * 4,
]

engine = alc.create_engine('sqlite:///bot_db')
session = alc_orm.sessionmaker(bind=engine)()


def add_word(user_id: int, word: str, translation: str) -> None:
    user_exists = not session.query(User).filter_by(id=user_id).first() is None
    if not user_exists:
        user = User(id=user_id)
        session.add(user)

    remember_time = round(time.time()) + INTERVALS[0]

    word = Word(
        user_id=user_id,
        word=word,
        translation=translation,
        remember_time=remember_time
    )
    session.add(word)

    session.commit()


# def check_words_to_remember() -> None:
#     user_exists = session.query(User).filter_by(id=24123).first() is None
#     if


# check_words_to_remember()
