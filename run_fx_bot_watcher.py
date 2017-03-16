# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricewatch.settings")
django.setup()

from pricealert.models import PriceAlert
import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    print(msg)
    print("Text Command: " + msg['text'])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='EURUSD', callback_data='EURUSD')],
                   [InlineKeyboardButton(text='USDJPY', callback_data='USDJPY')],
                   [InlineKeyboardButton(text='GBPUSD', callback_data='GBPUSD')],
               ])

    bot.sendMessage(chat_id, 'Select the quote item', reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    result = query_data + ": " + get_fx_live_rate(query_data)
    
    #for alert in PriceAlert.objects.filter(symbol=str(query_data),alert_status='1'):
    #    result += "\n" + str(alert)
    
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

        return "Bid: "rate.find('Bid').text + " / Ask: " + rate.find('Ask').text + " " + direction
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
 
