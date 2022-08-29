import sqlalchemy as alc
import sqlalchemy.orm as alc_orm

import time

from database.models import Word, User

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


def add_word(user_id: int, chat_id: int, word: str, translation: str) -> None:
    user_exists = not session.query(User).filter_by(id=user_id).first() is None
    print(chat_id)
    if not user_exists:
        user = User(id=user_id, chat_id=chat_id)
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


def change_is_waiting(user: User) -> bool:
    user.is_waiting = not user.is_waiting
    session.commit()

    return user.is_waiting


def get_words_to_remember() -> list:
    words = []

    users = session.query(User).filter_by(is_waiting=False)
    for user in users:
        word = get_word_to_remember(user.id)
        if word:
            words.append((word, user))

    return words


def get_word_to_remember(user_id: int) -> Word | None:
    """Получить первое слово для запоминания."""
    word = session.query(Word).filter_by(user_id=user_id).\
        order_by(Word.remember_time).first()

    if word.remember_time < time.time():
        return word
    return None


def update_word_status(word_id: int, is_right: bool) -> int:
    word = Word.query.get(word_id)

    if is_right:
        if word.status < 4:
            word.status += 1
    else:
        if word.status > 0:
            word.status -= 1

    word.remember_time = round(time.time()) + INTERVALS[word.status]

    return word.status
