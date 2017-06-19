#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import re
import os
from datetime import date, datetime

from market_watch.telegram import bot_sender
from market_watch.util import config_loader

# load config
config = config_loader.load() 

def get_sunday(input):
    d = input.toordinal()
    last = d - 6
    sunday = last - (last % 7)
    get_sunday = sunday + 7
    return date.fromordinal(get_sunday)

def get_fx_calendar():

    now = datetime.now()
    year = now.year
    start_of_week = ""
    passage = ""
    
    # if weekday, take last sunday
    if (now.isoweekday() <= 5):
        start_of_week = get_sunday(now).strftime("%m%d")
    # if saturday, take coming sunday
    elif (now.isoweekday() == 6):
        start_of_week = get_sunday(now).strftime("%m%d")
    # else, today is sunday (7)
    else:
        start_of_week = now.strftime("%m%d") 
    
    config.set("dailyfx", "calendar-year", str(year))
    config.set("dailyfx", "calendar-week", start_of_week)
    url = config.get("dailyfx", "calendar-url")

    print("Url: [" + url + "]")
    
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    for tr in soup.find_all('tr', {'data-importance': 'high'}):
           
        _date = tr.select('td')[1].text[:10]
        
        _timecheck = tr.select('td')[3].text[:2]
        _time = ""
        _event = ""
        
        if(_timecheck.isdigit()):
            _time = tr.select('td')[3].text[:5]
            _event = tr.select('td')[3].text[5:]
        else:
            _time = "NA"
            _event = tr.select('td')[3].text

        _converted_date = datetime.strptime(_date, '%Y-%m-%d')
        _dayname = _converted_date.strftime("%a")
        
        if (_converted_date.date() >= now.date()):
            passage = passage + "<b>" + _date + " (" + _dayname + ")" + "</b>" + " <i>@" + _time + "</i>" + "\n" + _event + "\n\n"
    
    if (passage == ""):
        passage = "No event for today."
    
    print("Passage: [" + passage + "]")
    return passage

def main():
    # sync top 100 list
    passage = "Major Market Events for today" + "\n\n" + get_fx_calendar()

    # Send a message to a chat room (chat room ID retrieved from getUpdates)
    bot_sender.broadcast(passage)

if __name__ == "__main__":
    main()        
        

