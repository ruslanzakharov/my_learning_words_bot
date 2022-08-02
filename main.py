import logging
import os

import telegram.ext as tg_ext

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = tg_ext.ApplicationBuilder().token(TOKEN).build()

    application.run_polling()
