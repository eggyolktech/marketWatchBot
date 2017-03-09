# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricewatch.settings")
django.setup()

# imdb process import
from pricealert.models import PriceAlert
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
import time
import sys
from datetime import date
from datetime import datetime

class Price:

    def __init__(self, symbol, last):
        self.symbol = symbol
        self.bid = 0.0000         
        self.ask = 0.0000
        self.high = 0.0000
        self.low = 0.0000
        self.last = last

def get_fx_rate_alerts():

    url = "https://rates.fxcm.com/RatesXML"

    #print("Url: [" + url + "]")
    
    r = requests.get(url)
    xml = r.text
    soup = BeautifulSoup(xml, 'xml')
    i=1
    
    #<Rate Symbol="EURUSD">
    #<Bid>1.05896</Bid>
    #<Ask>1.06001</Ask>
    #<High>1.06287</High>
    #<Low>1.05372</Low>
    #<Direction>0</Direction>
    #<Last>16:57:55</Last>
    #</Rate>
    # look in the main node for object's with attr=name, optionally look up attrs with regex
    
    for rate in soup.findAll('Rate'):
    
        i += 1
        price = Price(rate['Symbol'], rate.find('Last').text)
        price.bid = Decimal(rate.find('Bid').text)
        price.ask = Decimal(rate.find('Ask').text)
        price.high = Decimal(rate.find('High').text)
        price.low = Decimal(rate.find('Low').text)
        #print("Checking on Alerts on [" + price.symbol + "]....")
        if PriceAlert.objects.filter(symbol=str(price.symbol),alert_status='1'):
            for alert in PriceAlert.objects.filter(symbol=str(price.symbol),alert_status='1'):
                
                # get price operand to compare
                price_operand = get_price_operand(price, alert.quote)
                 
                if(price_operand and is_price_alert_triggered(price_operand, alert)):                    
                    passage = alert.get_message() + "\n" + alert.quote + " Price Now: " + str(price_operand) + " (" + price.last + " EST)"
                    print("Passage: [" + passage + "]")
                    send_to_tg_chatroom(passage)
                    alert.alert_status = '2'
                    alert.alert_date = datetime.now()
                    alert.alert_price = price_operand
                    alert.save()
                    
        else:
            a = None
            #print("No Price Alerts found on [" + price.symbol + "]") 
        
        if (i > 10):
            break
 
def get_price_operand(price, quote):
    
    price_operand = 0.0000
    
    if (quote == "Bid"):
        price_operand = price.bid
    elif (quote == "Ask"):
        price_operand = price.ask
    elif (quote == "High"):
        price_operand = price.high
    elif (quote == "Low"):
        price_operand = price.low
    else:
        print("Alert Quote Setup Incorrect: [" +  quote + "]")
        
    return price_operand   

def is_price_alert_triggered(price_operand, alert):
    
    left_operand = price_operand
    right_operand = alert.price_operand
    
    result = False
    print("Trigger Test: [" + alert.symbol + ": " + str(left_operand) + " " + alert.comparator + " " + str(right_operand) + "]")
    
    if (alert.comparator == ">"):
        result = (left_operand > right_operand)
    elif (alert.comparator == ">="):
        result = (left_operand >= right_operand)
    elif (alert.comparator == "<"):
        result = (left_operand < right_operand)
    elif (alert.comparator == "<="):
        result = (left_operand <= right_operand)
    else:
        result = False

    print("Trigger Result: [" + str(result) + "]")
    return result
        
def send_to_tg_chatroom(passage): 
    
    try:
        bot_id = "193192163:AAGC4RFnLmU7uJSbrJFPz1y36202O_NJcDU"
        result = urllib.request.urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": -172861420, "text": passage }).encode("utf-8")).read()
        print(result) 
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print( "Send Telegram Error: %s" % e )
  
while True:
    #do some serial sending here
    print("Price Watcher Interval: [" + str(datetime.now()) + "]");
    get_fx_rate_alerts()
    time.sleep(45)

    

# Send a message to a chat room (chat room ID retrieved from getUpdates)
#send_to_tg_chatroom(passage)

