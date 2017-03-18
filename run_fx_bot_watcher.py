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
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import random
from get_daily_fx_calendar import get_fx_calendar
from get_aastocks_hy_stats import get_aastocks_etf_stat, get_aastocks_hy_stat
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    print(msg)
    print("Text Command: " + msg['text'])
    
    command = msg['text'].split("@")[0]
    
    keyboard_list = []
    reply = ""
    
    if (command == "/fx"):
        keyboard_list = [
                       [InlineKeyboardButton(text='EURUSD', callback_data='EURUSD'), InlineKeyboardButton(text='GBPUSD', callback_data='GBPUSD'), InlineKeyboardButton(text='USDJPY', callback_data='USDJPY')],
                       [InlineKeyboardButton(text='AUDUSD', callback_data='AUDUSD'), InlineKeyboardButton(text='NZDUSD', callback_data='NZDUSD'), InlineKeyboardButton(text='USDCAD', callback_data='USDCAD')],
                       [InlineKeyboardButton(text='USDCHF', callback_data='USDCHF'), InlineKeyboardButton(text='EURJPY', callback_data='EURJPY'), InlineKeyboardButton(text='GBPJPY', callback_data='GBPJPY')],
                       [InlineKeyboardButton(text='EURGBP', callback_data='EURGBP'), InlineKeyboardButton(text='AUDNZD', callback_data='AUDNZD'), InlineKeyboardButton(text='USDCNH', callback_data='USDCNH')],
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
        
        passage = 'Please tap on the Top 10 list to show \n\n' + ' /ttETF - High Dividends ETF ' + u'\U0001F4B0' + '\n\n' + ' /ttBanks - High Dividends Banks ' + u'\U0001F3E6' + '\n\n' + ' /ttREIT - High Dividends REIT ' + u'\U0001F3E2' + '\n\n' + ' /ttCong - Conglomerates ' + u'\U0001F310'
        
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
      
    elif (command == "/cal"):
    
        bot.sendMessage(chat_id, '<i>Retreiving Event Calendar...</i>', parse_mode='HTML')
        passage = get_fx_calendar()
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
    
    elif (command == "/funny"):
        
        funny_list = ['http://cdn2.ettoday.net/images/1613/1613045.jpg', 'https://i0.wp.com/farm6.staticflickr.com/5462/9214555634_bb1859cd18.jpg', 'https://i1.wp.com/farm8.staticflickr.com/7412/9211776213_2229c5f440.jpg', 'https://i0.wp.com/farm6.staticflickr.com/5338/9214716454_19304819fe.jpg', 'http://i.imgur.com/1yTUg.jpg']
        
        f = urllib.request.urlopen(random.choice(funny_list))
        bot.sendPhoto(chat_id, f)     
    elif (command.startswith("/tt")):
    
        bot.sendMessage(chat_id, '<i>Retreiving Top 10 List...</i>', parse_mode='HTML')
        
        industry = command[3:]
        
        if (industry == "ETF"):
            passage = get_aastocks_etf_stat(config.get("aastocks","hy-url-etf"))
            bot.sendMessage(chat_id, passage, parse_mode='HTML')        
        else:
            bot.sendMessage(chat_id, '<i>Sorry! Top 10 List does not exist for specified target [' + industry + '] </i>', parse_mode='HTML')
    else:
        menu = '金鑊鏟 Bot v1.0.3 \n\n' + ' /fx - FX Quote ' + u'\U0001F4B9' + '\n\n' + ' /idq - Index Quote ' + u'\U0001F4C8' + '\n\n' + ' /cmd - Commodities Quote ' + u'\U0001F30E' + '\n\n' + ' /cal - Coming Events ' + u'\U0001F4C5' + '\n\n' + ' /funny - Time will tell... ' + u'\U0000231B'
    
        bot.sendMessage(chat_id, menu)
        
def on_callback_query(msg):

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    # if query data is available
    if query_data:
    
        result = query_data + ": " + get_fx_live_rate(query_data)
        bot.answerCallbackQuery(query_id, text=result)
   
def get_fx_live_rate(quote):

    url = "https://rates.fxcm.com/RatesXML"
   
    r = requests.get(url)
    xml = r.text
    soup = BeautifulSoup(xml, 'xml')

    #<Rate Symbol="EURUSD">
    #<Bid>1.05896</Bid>
    #<Ask>1.06001</Ask>
    #<High>1.06287</High>
    #<Low>1.05372</Low>
    #<Direction>0</Direction>
    #<Last>16:57:55</Last>
    #</Rate>
    # look in the main node for object's with attr=name, optionally look up attrs with regex
    
    rate = soup.find('Rate', {'Symbol': quote})
    live_rate = ''
    
    if(rate):
        
        direction = u'\U000027A1'
        
        if (int(rate.find('Direction').text) > 0):
            direction = u'\U00002B06'
        elif (int(rate.find('Direction').text) < 0):
            direction = u'\U00002B07'

        return "Bid: " + rate.find('Bid').text + " / Ask: " + rate.find('Ask').text + " " + direction
    else:
        return "No live rate is returned."
    
TOKEN = "193192163:AAGC4RFnLmU7uJSbrJFPz1y36202O_NJcDU" # get token from command-line

bot = telepot.Bot(TOKEN)
print(bot.getMe())
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)
 
