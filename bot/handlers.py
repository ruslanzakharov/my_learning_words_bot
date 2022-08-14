import telegram as tg
import telegram.ext as tg_ext

import db

START, ENG_WORD, RU_WORD = range(3)


async def start(
    update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
) -> int:
    keyboard = [['Новое слово']]
    reply_markup = tg.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text('ПРИВЕТ!!!')
    await update.message.reply_text(
        f'Привет, {update.effective_user.first_name}. Я помогу тебе запомнить как можно больше иностранных слов!',
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


def setup_handlers(application: tg_ext.Application) -> None:
    # start_handler = tg_ext.CommandHandler('start', start)

    conv_handler = tg_ext.ConversationHandler(
        entry_points=[tg_ext.CommandHandler('start', start)],
        states={
            START: [
                tg_ext.MessageHandler(
                    tg_ext.filters.Regex('^(Новое слово|Старое слово)$'),
                    new_word,
                )
            ],
            ENG_WORD: [
                tg_ext.MessageHandler(tg_ext.filters.TEXT, new_word_eng)
            ],
            RU_WORD: [tg_ext.MessageHandler(tg_ext.filters.TEXT, new_word_ru)],
        },
        fallbacks=[tg_ext.CommandHandler('start', start)],
    )

    # application.add_handler(start_handler)
    application.add_handler(conv_handler)
