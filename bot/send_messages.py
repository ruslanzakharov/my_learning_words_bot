import telegram.ext as tg_ext

import schedule

from database import db


def send_words(bot: tg_ext.Application.bot) -> None:
    """Отправляет слова на русском для перевода пользователем."""

    words = db.get_words_to_remember()

    for word in words:
        word_eng = word[0].word
        user = word[1]

        bot.send_message(user.chat_id, word_eng)
        db.change_is_waiting(user)


def setup(bot: tg_ext.Application.bot) -> None:
    schedule.every(10).minutes.do(send_words, bot=bot)
