# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricewatch.settings")
django.setup()

from pricealert.models import PriceAlert
import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from decimal import Decimal
import urllib.request
import random
from get_daily_fx_calendar import get_fx_calendar
from get_aastocks_hy_stats import get_aastocks_etf_stat, get_aastocks_hy_stat
from get_fx_live_rate import get_fx_live_rate, get_dxy_live_rate
from get_aastocks_chart import get_hkg_chart_by_type
import configparser

from classes.TimeFrame import TimeFrame

config = configparser.ConfigParser()
config.read('config.properties')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    print(msg)
    print("Text Command: " + msg['text'])
    
    command = msg['text'].split("@")[0]
    EL = '\n\n'
    
    keyboard_list = []
    reply = ""
    
    if (command == "/fx"):
        keyboard_list = [
                       [InlineKeyboardButton(text='EURUSD', callback_data='EURUSD'), InlineKeyboardButton(text='GBPUSD', callback_data='GBPUSD'), InlineKeyboardButton(text='USDJPY', callback_data='USDJPY')],
                       [InlineKeyboardButton(text='AUDUSD', callback_data='AUDUSD'), InlineKeyboardButton(text='NZDUSD', callback_data='NZDUSD'), InlineKeyboardButton(text='USDCAD', callback_data='USDCAD')],
                       [InlineKeyboardButton(text='USDCHF', callback_data='USDCHF'), InlineKeyboardButton(text='EURJPY', callback_data='EURJPY'), InlineKeyboardButton(text='GBPJPY', callback_data='GBPJPY')],
                       [InlineKeyboardButton(text='EURGBP', callback_data='EURGBP'), InlineKeyboardButton(text='AUDNZD', callback_data='AUDNZD'), InlineKeyboardButton(text='USDCNH', callback_data='USDCNH')],
                       [InlineKeyboardButton(text='DXY', callback_data='DXY')]
               ]
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
        bot.sendMessage(chat_id, 'Please tap on the FX pair to quote', reply_markup=keyboard)
        
    elif (command == "/idq"):
        keyboard_list = [
                       [InlineKeyboardButton(text='HSI', callback_data='HKG33'), InlineKeyboardButton(text='NIKKEI', callback_data='JPN225'), InlineKeyboardButton(text='DJI', callback_data='US30')],
                       [InlineKeyboardButton(text='SPX', callback_data='SPX500'), InlineKeyboardButton(text='NASDAQ', callback_data='NAS100'), InlineKeyboardButton(text='FTSE', callback_data='UK100')],
                       [InlineKeyboardButton(text='DAX', callback_data='GER30'), InlineKeyboardButton(text='IBEX', callback_data='ESP35'), InlineKeyboardButton(text='CAC', callback_data='FRA40')],
                       [InlineKeyboardButton(text='S&P/ASX 200', callback_data='AUS200'), InlineKeyboardButton(text='Euro Stoxx 50', callback_data='EUSTX50'), InlineKeyboardButton(text='Bund', callback_data='Bund')],
               ]
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
        bot.sendMessage(chat_id, 'Please tap on the Index to quote', reply_markup=keyboard)
        
    elif (command == "/cmd"):
        keyboard_list = [
                       [InlineKeyboardButton(text='WTI Crude', callback_data='USOil'), InlineKeyboardButton(text='Brent Oil', callback_data='UKOil'), InlineKeyboardButton(text='Gold', callback_data='XAUUSD')],
                       [InlineKeyboardButton(text='Silver', callback_data='XAGUSD'), InlineKeyboardButton(text='Natural Gas', callback_data='NGAS'), InlineKeyboardButton(text='Copper', callback_data='Copper')],
               ]
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
        bot.sendMessage(chat_id, 'Please tap on the Commodity to quote', reply_markup=keyboard) 
  
    elif (command == "/top10"):
    
        menuitemlist = [{'command': '/ttETF', 'desc': 'High Dividends ETF', 'icon': u'\U0001F4B0'},
                    {'command': '/ttBanks', 'desc': 'High Dividends Banks', 'icon': u'\U0001F3E6'},
                    {'command': '/ttREIT', 'desc': 'High Dividends REIT', 'icon': u'\U0001F3E2'},
                    {'command': '/ttCong', 'desc': 'High Dividends Conglomerates', 'icon': u'\U0001F310'},
        ]
 
        passage = 'Please tap on the Top 10 list to show '
        
        for menuitem in menuitemlist:
            passage = passage + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
 
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
      
    elif (command == "/cal"):
    
        bot.sendMessage(chat_id, '<i>Retreiving Event Calendar...</i>', parse_mode='HTML')
        passage = get_fx_calendar()
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
    
    elif (command.startswith("/tt")):
    
        bot.sendMessage(chat_id, '<i>Retreiving Top 10 List...</i>', parse_mode='HTML')
        
        industry = command[3:]
        
        if (industry == "ETF"):
            passage = get_aastocks_etf_stat(config.get("aastocks","hy-url-etf"))
        elif (industry == "Banks"):
            passage = get_aastocks_hy_stat(config.get("aastocks-hy-industry","hy-url-banks"), "Banks")
        elif (industry == "REIT"):
            passage = get_aastocks_hy_stat(config.get("aastocks-hy-industry","hy-url-reits"), "REIT")
        elif (industry == "Cong"):   
            passage = get_aastocks_hy_stat(config.get("aastocks-hy-industry","hy-url-conglomerates"), "Conglomerates")
        else:
            passage = '<i>Sorry! Top 10 List not found for target [' + industry + '] </i>'
            
        passage = passage + 'Back to Top 10 Menu - /top10'
        bot.sendMessage(chat_id, passage, parse_mode='HTML') 

    elif (command.startswith("/q")):
    
        tf = command[2:3]
        code = command[3:]
        timeframe = TimeFrame.DAILY
        
        menu = '<b>Quote AAStocks Charts Command</b>'
        
        menuitemlist = [{'command': '/qM[StockCode]', 'desc': 'Quote Monthly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qw[StockCode]', 'desc': 'Quote Weekly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qd[StockCode]', 'desc': 'Quote Daily Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qh[StockCode]', 'desc': 'Quote Hourly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qm[StockCode]', 'desc': 'Quote Minutes Chart', 'icon': u'\U0001F4C8'},
        ]

        for menuitem in menuitemlist:
            menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
        
        if (tf == "M"):
            timeframe = TimeFrame.MONTHLY
        elif (tf.lower() == "w"):
            timeframe = TimeFrame.WEEKLY
        elif (tf.lower() == "d"):
            timeframe = TimeFrame.DAILY
        elif (tf.lower() == "h"):
            timeframe = TimeFrame.HOURLY
        elif (tf.lower() == "m"):
            timeframe = TimeFrame.MINUTE
        else:        
            bot.sendMessage(chat_id, menu, parse_mode='HTML') 
            return

        if code:
            bot.sendMessage(chat_id, '<i>Retrieving AAStocks Chart...</i>', parse_mode='HTML')
            f = urllib.request.urlopen(get_hkg_chart_by_type(code, timeframe))
            bot.sendPhoto(chat_id, f)
        else:
            stockcode = random.choice(["2628", "939", "2800", "8141", "AAPL", "GOOG", "GS"])
            passage = "<i>Usage:</i> " + command + "[StockCode] (e.g. " + command + stockcode + ")"
            bot.sendMessage(chat_id, passage, parse_mode='HTML') 
        
    else:    
    
        menuitemlist = [{'command': '/fx', 'desc': 'FX Quote', 'icon': u'\U0001F4B9'},
                        {'command': '/idq', 'desc': 'Index Quote', 'icon': u'\U0001F310'},
                        {'command': '/cmd', 'desc': 'Commodities Quote', 'icon': u'\U0001F30E'},
                        {'command': '/cal', 'desc': 'Coming Market Events', 'icon': u'\U0001F4C5'},
                        {'command': '/top10', 'desc': 'Top 10 List', 'icon': u'\U0001F51F'},
                        {'command': '/q', 'desc': 'Quick Chart', 'icon': u'\U0001F4C8'},
        ]
        
        menu = '金鑊鏟 Bot v1.0.6'
        
        for menuitem in menuitemlist:
            menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
    
        bot.sendMessage(chat_id, menu)
        
def on_callback_query(msg):

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    result = "No live rate is available"

    # if query data is available
    if query_data:
    
        if query_data == "DXY":
            result = query_data + ": " + get_dxy_live_rate()
        else:  
            result = query_data + ": " + get_fx_live_rate(query_data)
        
        bot.answerCallbackQuery(query_id, text=result)
    
TOKEN = config.get("telegram","bot-id") # get token from command-line

bot = telepot.Bot(TOKEN)
print(bot.getMe())
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)
 
