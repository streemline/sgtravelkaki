import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from api.BusApi import BusApi

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """message send for Command: start"""
    update.message.reply_text('Hi!')


def get_help(bot, update):
    """message send for Command: help"""
    update.message.reply_text('Help!')

def bus_stop(bot, update):
    """message send for Command: busstop"""
    split_arr = update.message.text.split()
    if len(split_arr) == 2:
        bus_api = BusApi()
        msg = bus_api.get_bus_arrival_msg(split_arr[1])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')
    else:
        update.message.reply_text("Please provie me with the bus stop number.\nE.g. /busstop 67329")

def echo(bot, update):
    """message send for user input"""
    update.message.reply_text(update.message.text)


def handle_error(bot, update, error):
    """message send for when error occurs"""
    LOGGER.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    """Main def"""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("BOT-TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("busstop", bus_stop))
    dispatcher.add_handler(CommandHandler("help", get_help))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dispatcher.add_error_handler(handle_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
