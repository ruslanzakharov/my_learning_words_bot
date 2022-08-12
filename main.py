import logging
import os

import telegram.ext as tg_ext

from bot import handlers

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    application = tg_ext.ApplicationBuilder().token(TOKEN).build()

    handlers.setup_handlers(application)

    application.run_polling()


if __name__ == '__main__':
    main()
