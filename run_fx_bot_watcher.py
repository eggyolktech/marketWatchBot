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
    EL = '\n\n'
    
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
        
    else:    
    
        menuitemlist = [{'command': '/fx', 'desc': 'FX Quote', 'icon': u'\U0001F4B9'},
                        {'command': '/idq', 'desc': 'Index Quote', 'icon': u'\U0001F4C8'},
                        {'command': '/cmd', 'desc': 'Commodities Quote', 'icon': u'\U0001F30E'},
                        {'command': '/cal', 'desc': 'Coming Market Events', 'icon': u'\U0001F4C5'},
                        {'command': '/top10', 'desc': 'Top 10 List', 'icon': u'\U0001F51F'},
        ]
        
        menu = '金鑊鏟 Bot v1.0.4'
        
        for menuitem in menuitemlist:
            menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
    
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
    
TOKEN = config.get("telegram","bot-id") # get token from command-line

bot = telepot.Bot(TOKEN)
print(bot.getMe())
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)
 
