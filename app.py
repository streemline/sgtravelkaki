# -*- coding: utf-8 -*-
"""Main bot module"""
import os
import logging
import json
from telegram import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineQueryResultArticle,InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler
from api import botan
from api.bus import Bus
from api.streetview import StreetView
from api.nearby import Nearby
from api.emojicode import EmojiCode
from api.businfo import BusInfo

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
EMOJICODE = EmojiCode()

TELEGRAM_TOKEN = ''
PORT = int(os.environ.get('PORT', '5000'))
BOTAN_TOKEN = ''

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """message send for Command: start"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/start')
    msg = 'Whats up'+ EMOJICODE.sunglasses() +', what do you want me to do for you ah?'
    bot.send_message(chat_id=update.message.chat.id, text=msg)

def get_help(bot, update):
    """message send for Command: help"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/help')
    msg = 'Let me show you the *command list* ah \n\n'
    msg += '/busstop - Show bus arrival info' + EMOJICODE.busstop() + EMOJICODE.info() + '\n'
    msg += '/nearby - Show nearby bus stops '+ EMOJICODE.busstop() + '\n'
    msg += '/businfo - Show bus info' + EMOJICODE.bus() + EMOJICODE.info() + '\n'
    msg += '/emoji - Show emoji meaning ' +  EMOJICODE.smile() +'\n'
    msg += '/mrtmap - Show MRT map ' +  EMOJICODE.station() +'\n'
    msg += '/grabpromo - Show grab promotions \n'
    msg += '/uberpromo - Show uber promotions \n'
    msg += '/close - Close reply keyboard' + EMOJICODE.keyboard() +'\n'
    msg += '/help - Show help list' +  EMOJICODE.sos() +'\n'
    msg += '/start - To start from beginning\n'
    bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')

def bus_stop(bot, update):
    """message send for Command: busstop"""
    split_arr = update.message.text.split()
    bus = Bus()
    if len(split_arr) == 2:
        botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/busstop all')
        msg = bus.get_bus_arrival_msg(split_arr[1])
        reply_markup = bus_arrival_markup(split_arr[1])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown',
        reply_markup=reply_markup)
    elif len(split_arr) == 3:
        botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/busstop single')
        msg = bus.get_bus_arrival_msg(split_arr[1], split_arr[2])
        reply_markup = bus_arrival_markup(split_arr[1] + ' ' + split_arr[2])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown',
        reply_markup=reply_markup)
    else:
        botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/busstop')
        msg = 'Tell me the bus stop no in this format ah. \n\n'
        msg += '*Format* : \n- /busstop <bus stop no> <bus no> (optional) \n\n'
        msg += '*Example* : \n- /busstop 67329 \n- /busstop 67329 163 \n\n'
        msg += 'You can also send me a inline query by typing @sgtravelkakibot followed '
        msg += 'by the bus stop name or code.'
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Try inline query", switch_inline_query_current_chat='67321')]
        ])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown',
        reply_markup=reply_markup)

def nearby_bus_stop(bot, update):
    """message send for Command: nearby"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/nearby')
    location_keyboard = KeyboardButton(text="send_location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]], resize_keyboard=True,
    one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat.id, text="Please tell me where you are.",
    reply_markup=reply_markup)

def bus_info(bot, update):
    """message send for Command: businfo"""
    split_arr = update.message.text.split()
    bus_info = BusInfo()
    if len(split_arr) == 2:
        botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/businfo bus')
        msg = bus_info.get_bus_info_msg(split_arr[1])
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')
    else:
        botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/businfo')
        msg = 'Tell me the bus no in this format ah. \n\n'
        msg += '*Format* : \n- /businfo <bus no>\n\n'
        msg += '*Example* : \n- /businfo 50 \n- /businfo 163'
        bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')

def mrt_map(bot, update):
    """message send for Command: mrtmap"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/mrtmap')
    msg = '*MRT map*\n\n'
    msg += 'Click [here](https://goo.gl/xqRlx7)'
    bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')

def emoji_meaning(bot, update):
    """message send for Command: emoji"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/emoji')
    msg = 'Let me tell you what each emoji means ah. \n\n'
    msg += EMOJICODE.smile() + ' - This one means got seats in bus ah. \n'
    msg += EMOJICODE.sweating() + ' - This one means no seats liao. So need to stand ah. \n'
    msg += EMOJICODE.angry() + ' - This one is the worst ah. No seats and no place to stand. '
    msg += 'Wait for next bus ba. \n'
    msg += EMOJICODE.wheelchair() + ' - This one means the bus is wheelchair accessible one.'
    bot.send_message(chat_id=update.message.chat.id, text=msg)

def close_command(bot, update):
    """message send for Command: close"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, '/close')
    bot.send_message(chat_id=update.message.chat.id, text="Okay close liao.", reply_markup=ReplyKeyboardRemove())

def inlinequery(bot, update):
    """Inline query message handling"""
    query = str(update.inline_query.query).lower()
    results = list()  
    bus = Bus()
    with open('data/busstop.json') as json_data:
        bus_stop_list = json.load(json_data)
        for bus_stop in bus_stop_list:
            if query in bus_stop['no'].lower() or query in bus_stop['name'].lower():
                reply_markup = bus_arrival_inline_markup(bus_stop['no'])
                results.append(InlineQueryResultArticle(id=bus_stop['no'],
                title=bus_stop['no'] + ' - ' + bus_stop['name'], 
                description=bus_stop['name'], reply_markup=reply_markup,
                input_message_content=InputTextMessageContent('Click refresh to get bus timing.')))
            if len(results) == 30:
                update.inline_query.answer(results)
                break
        update.inline_query.answer(results)

def grab_promo(bot, update):
    msg = "*All Grab services* \n" 
    bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')

def uber_promo(bot, update):
    msg = "*Uber Promotions* \n" 
     bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown')

def echo(bot, update):
    """message send for user input"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, 'echo')
    bot.send_message(chat_id=update.message.chat.id, 
    text="I'm still not smart enough to understand what you are saying ah.")

def location(bot, update):
    """message send for location callback"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, 'location-callback')
    lat = update.message.location.latitude
    lng = update.message.location.longitude
    nearby = Nearby()
    nearest_3_list = nearby.get_nearest_three_bus_stops(lat,lng)
    msg = nearby.get_nearby_cmd_msg(nearest_3_list)
    button_list = [
        [InlineKeyboardButton(EMOJICODE.busstop() + ' ' + nearest_3_list[0]['no'],
        callback_data='nearby ' + nearest_3_list[0]['no'])],
        [InlineKeyboardButton(EMOJICODE.busstop() + ' ' + nearest_3_list[1]['no'],
        callback_data='nearby ' + nearest_3_list[1]['no'])],
        [InlineKeyboardButton(EMOJICODE.busstop() + ' ' + nearest_3_list[2]['no'],
        callback_data='nearby ' + nearest_3_list[2]['no'])]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode='Markdown',
    reply_markup=reply_markup)


def inline_button(bot, update):
    """Inline button message handling"""
    callback = update.callback_query
    data_arr = callback.data.split()
    bus = Bus()   
    if data_arr[0] == 'refresh':
        if len(data_arr) == 2:
            botan.track(BOTAN_TOKEN, callback.message.chat.id, callback, 'inline-btn-refresh-all')
            msg = bus.get_bus_arrival_msg(data_arr[1])
            reply_markup = bus_arrival_markup(data_arr[1])
        else:
            botan.track(BOTAN_TOKEN, callback.message.chat.id, callback, 'inline-btn-refresh-single')
            msg = bus.get_bus_arrival_msg(data_arr[1], data_arr[2])
            reply_markup = bus_arrival_markup(data_arr[1] + ' ' + data_arr[2])
        bot.editMessageText(chat_id=callback.message.chat.id,
        message_id=callback.message.message_id, text=msg,
        parse_mode='Markdown', reply_markup=reply_markup)
        bot.answerCallbackQuery(callback_query_id=callback.id,
        text='Bus timing updated')
    elif data_arr[0] == 'inline-mode-refresh':
        msg = bus.get_bus_arrival_msg(data_arr[1])
        reply_markup = bus_arrival_inline_markup(data_arr[1])
        bot.editMessageText(inline_message_id =callback.inline_message_id, text=msg,
        parse_mode='Markdown', reply_markup=reply_markup)
        bot.answerCallbackQuery(callback_query_id=callback.id,
        text='Bus timing updated')
    elif data_arr[0] == 'streetview':
        streetview = StreetView()
        bus_stop_detail = bus.get_bus_stop_detail(data_arr[1])
        if bus_stop_detail is not None:
            botan.track(BOTAN_TOKEN, callback.message.chat.id, callback, 'inline-btn-streetview')
            latlng = streetview.get_lat_lng_str(bus_stop_detail)
            streetview_img_url = streetview.form_street_view_img_url(latlng)
            bot.send_photo(chat_id=callback.message.chat.id,
            photo=streetview_img_url, caption=bus_stop_detail['name'])
            bot.answerCallbackQuery(callback_query_id=callback.id,
            text='Bus stop photo shown')
        else:
            botan.track(BOTAN_TOKEN, callback.message.chat.id, callback, 'inline-btn-streetview-not-found')
            bot.send_message(chat_id=callback.message.chat.id,
            message_id=callback.message.message_id, text='Bus stop not found leh.') 
            bot.answerCallbackQuery(callback_query_id=callback.id,
            text='No bus stop photo found')
    elif data_arr[0] == 'nearby':
        botan.track(BOTAN_TOKEN, callback.message.chat.id, callback, 'inline-btn-nearby')
        msg = bus.get_bus_arrival_msg(data_arr[1])
        reply_markup = bus_arrival_markup(data_arr[1])
        bot.send_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id, 
        text=msg, parse_mode='Markdown', reply_markup=reply_markup)
        bot.answerCallbackQuery(callback_query_id=callback.id,
        text='Bus timing shown')    

def handle_error(bot, update, error):
    """message send for when error occurs"""
    botan.track(BOTAN_TOKEN, update.message.chat.id, update.message, 'error')
    LOGGER.warn('Update "%s" caused error "%s"' % (update, error))


def bus_arrival_markup(data_msg):
        """Inline Keyboard Markup for busstop command"""
        button_list = [
            [InlineKeyboardButton("Refresh", callback_data='refresh '+ data_msg),
            InlineKeyboardButton("Street View", callback_data='streetview '+ data_msg)],
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        return reply_markup

def bus_arrival_inline_markup(bus_no):
    """Inline Keyboard Markup for inline command"""
    button_list = [
        [InlineKeyboardButton("Refresh", callback_data='inline-mode-refresh '
        + bus_no)]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def main():
    """Main function"""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN)
    updater.bot.set_webhook("https://app-name.herokuapp.com/" + TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("busstop", bus_stop))
    dispatcher.add_handler(CommandHandler("nearby", nearby_bus_stop))
    dispatcher.add_handler(CommandHandler("businfo", bus_info))
    dispatcher.add_handler(CommandHandler("mrtmap", mrt_map))
    dispatcher.add_handler(CommandHandler("grabpromo", grab_promo))
    dispatcher.add_handler(CommandHandler("uberpromo", uber_promo))
    dispatcher.add_handler(CommandHandler("emoji", emoji_meaning))
    dispatcher.add_handler(CommandHandler("close", close_command))
    dispatcher.add_handler(CommandHandler("help", get_help))

    # on inline button callback
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_button))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    #on location callback
    dispatcher.add_handler(MessageHandler(Filters.location, location))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

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
