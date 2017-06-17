#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

from market_watch.common.AastocksConstants import *
from market_watch.telegram import bot_sender

def get_aastocks_calendar():

    today = datetime.today().strftime('%Y/%m/%d')
    url = "http://www.aastocks.com/tc/stocks/market/calendar.aspx"

    print("Url: [" + url + "]")
    
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    passage = ""
    table = soup.find_all('div', {"class" : "grid_11"})[0].find_all('table')[3]
    is_today = False    
    
    #today = "2017/05/08"
    
    for tr in table.find_all('tr'):
        
        if (not is_today and len(tr.find_all('td')) == 1):
            if (today == tr.find_all('td')[0].text.strip()):
                is_today = True
        elif (is_today and len(tr.find_all('td')) == 1):
            # loop end
            break
        elif (is_today):
            passage = passage + tr.find_all('td')[0].text + " (" + tr.find_all('td')[1].text +")" + EL + tr.find_all('td')[3].text + DEL

    if (passage == ""):
        passage = "No Result Announcement for " + today + ""
    else:
        passage = "<i>Result Announcement for " + today + "</i>" + DEL + passage
    
    print("Passage: [" + str(passage.encode('utf-8')) + "]")
    return passage

def main():
    # sync top 100 list
    passage = get_aastocks_calendar()

    # Send a message to a chat room (chat room ID retrieved from getUpdates)
    bot_sender.broadcast(passage)

if __name__ == "__main__":
    main()        
        

