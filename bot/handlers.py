import telegram as tg
import telegram.ext as tg_ext

import db

START, ENG_WORD, RU_WORD, WORD_CHECK = range(4)


async def start(
    update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> int:
    keyboard = [['Новое слово']]
    reply_markup = tg.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        f'Привет, {update.effective_user.first_name}.'
        f' Я помогу тебе запомнить как можно больше иностранных слов!',
        reply_markup=reply_markup,
    )
    return START


async def new_word(
    update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text('Введите слово на английском')

    return ENG_WORD


async def new_word_eng(
    update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['eng_word'] = update.message.text

    await update.message.reply_text('Введите слово на русском')

    return RU_WORD


async def new_word_ru(
    update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> int:
    ru_word = update.message.text
    eng_word = context.user_data['eng_word']
    user_id = update.effective_user.id

    db.add_word(user_id, eng_word, ru_word)

    keyboard = [['Новое слово']]
    reply_markup = tg.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text('Добавлено!', reply_markup=reply_markup)

    return START


async def check_user_answer(
        update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> None:
    word = db.get_word_to_remember(update.effective_user.id)
    context.user_data['word_id'] = word[2]

    keyboard = [['Да', 'Нет']]
    reply_markup = tg.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        f'''Перевод: {word[0]}
        Вы ответили правильно?''',
        reply_markup=reply_markup
    )
    return WORD_CHECK


async def check_user_answer_new_word(
    update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> None:
    is_right = update.message.text == 'Да'
    db.update_word_status(context.user_data['word_id'], is_right)

    # Сделать: Получить новое слово, если такое есть Либо предложить ввести новое слово


def setup_handlers(application: tg_ext.Application) -> None:
    conv_handler = tg_ext.ConversationHandler(
        entry_points=[tg_ext.CommandHandler('start', start)],
        states={
            START: [
                tg_ext.MessageHandler(
                    tg_ext.filters.Regex('^Новое слово$'),
                    new_word)
            ],
            ENG_WORD: [
                tg_ext.MessageHandler(tg_ext.filters.TEXT, new_word_eng)
            ],
            RU_WORD: [
                tg_ext.MessageHandler(tg_ext.filters.TEXT, new_word_ru)
            ],
        },
        fallbacks=[tg_ext.CommandHandler('start', start)],
    )

    check_word_conv_handler = tg_ext.ConversationHandler(
        entry_points=[
            tg_ext.MessageHandler(tg_ext.filters.TEXT, check_user_answer)
        ],
        states={
            WORD_CHECK: [
                tg_ext.MessageHandler(
                    tg_ext.filters.Regex('^(Да|Нет)$'),
                    check_user_answer_new_word)
            ],
        },
        # Сделать: написать fallbacks
    )

    application.add_handler(conv_handler)
    application.add_handler(check_word_conv_handler)
