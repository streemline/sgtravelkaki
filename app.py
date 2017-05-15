import logging
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from api.busapi import BusApi

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
    bus_api = BusApi()
    if len(split_arr) == 2:
        msg = bus_api.get_bus_arrival_msg(split_arr[1])
        reply_markup = bus_arrival_markup(split_arr[1])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown',
        reply_markup=reply_markup)
    elif len(split_arr) == 3:
        msg = bus_api.get_bus_arrival_msg(split_arr[1], split_arr[2])
        reply_markup = bus_arrival_markup(split_arr[1] + ' ' + split_arr[2])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown',
        reply_markup=reply_markup)
    else:
        msg = 'Please provide me with the bus stop number.'
        msg += '\nFormat - /busstop <bus stop no> <bus no>(optional)'
        msg += '\nExample - /busstop 67329 or /busstop 67329 163'
        bot.send_message(chat_id=update.message.chat.id, text=msg)

def nearby_bus_stop(bot, update):
    update.message.reply_text('nearby')

def bus_info(bot, update):
    update.message.reply_text('bus info')

def echo(bot, update):
    """message send for user input"""
    update.message.reply_text(update.message.text)


def inline_button(bot, update):
    callback = update.callback_query
    data_arr = callback.data.split()
    if data_arr[0] == 'refresh':
        bus_api = BusApi()
        if len(data_arr) == 2:
            msg = bus_api.get_bus_arrival_msg(data_arr[1])
            reply_markup = bus_arrival_markup(data_arr[1])
        else:
            msg = bus_api.get_bus_arrival_msg(data_arr[1], data_arr[2])
            reply_markup = bus_arrival_markup(data_arr[1] + ' ' + data_arr[2])
        bot.editMessageText(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
        text=msg, parse_mode='Markdown',reply_markup=reply_markup)

def handle_error(bot, update, error):
    """message send for when error occurs"""
    LOGGER.warn('Update "%s" caused error "%s"' % (update, error))


def bus_arrival_markup(data_msg):
        button_list = [
            [InlineKeyboardButton("Refresh", callback_data='refresh '+ data_msg),
            InlineKeyboardButton("Street View",  callback_data='streetview '+ data_msg)],
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        return reply_markup


def main():
    """Main def"""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("busstop", bus_stop))
    dispatcher.add_handler(CommandHandler("nearby", nearby_bus_stop))
    dispatcher.add_handler(CommandHandler("businfo", bus_info))
    dispatcher.add_handler(CommandHandler("help", get_help))
    dispatcher.add_handler(CommandHandler("restart", start))

    updater.dispatcher.add_handler(CallbackQueryHandler(inline_button))

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
