"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
"""

import schedule, time
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5524943032:AAEZdiiNJ0JgQvCIf4py3Z9omNpwKRQiYJY'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Cazzo vuoi oh')

boss = None

def reset(update, context):
    global boss
    boss = None

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def message_handler(update, context):
    """Echo the user message."""
    text = update.message.text.lower() or ''

    global boss

    if text == "simione":
        update.message.reply_text('Mauro è il re delle simie!')
    elif text in ["simia", "scimmia", "simmia"]:
        if boss is None:
            boss = update.message.from_user.first_name
            update.message.reply_text('Per oggi sei TU il Queer delle Simie!')
        else:
            update.message.reply_text(boss + ' è il Queer delle Simie!')



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reset", reset))
    #dp.add_handler(CommandHandler("porcodio", porcodio))
    #dp.add_handler(CommandHandler("simia", simia))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://scimiapazza.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':

    # Every day at 12am or 00:00 time bedtime() is called.
    schedule.every().day.at("00:00").do(reset)

    main()

    # Loop so that the scheduling task
    # keeps on running all time.
    #while True:
        # Checks whether a scheduled task
        # is pending to run or not
    #    schedule.run_pending()
    #    time.sleep(1)
