#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import sys
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

def get_fx_calendar_notice():

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
        _actual = "NA" if tr.select('td')[5].text == "" else tr.select('td')[5].text
        _forecast = "NA" if tr.select('td')[6].text == "" else tr.select('td')[6].text
        _previous = "NA" if tr.select('td')[7].text == "" else tr.select('td')[7].text
        
        _cdate = datetime.strptime(_date, '%Y-%m-%d')

        if (_cdate.date() >= now.date() and _timecheck.isdigit()):
            
            _time = tr.select('td')[3].text[:5]
            _event = tr.select('td')[3].text[5:]
            _cdate = datetime.strptime(_date, '%Y-%m-%d')
            _cdatetime = datetime.strptime(_date + _time, '%Y-%m-%d%H:%M')
            _dayname = _cdate.strftime("%a")
            _rdatetime = now
            #_rdatetime = datetime.strptime("2017-10-17 17:15:05", '%Y-%m-%d %H:%M:%S')
            _hd = (_rdatetime - _cdatetime).total_seconds()/60

            if (_hd > 0 and _hd < 15):
                #print(_date + _time + " - " + _event + " (" + _actual + "," + _forecast + "," + _previous + ")")        
                passage = passage + "<b>" + u'\U0001F525' + " Event</b>" + " <i>@" + _time + "</i>" + "\n" + _event + "\n" + "(Actual: " + _actual + ", Forecast: " + _forecast + ", Previous: " + _previous + ")" + "\n\n"
            elif (_hd <= 0 and _hd > -20):
                passage = passage + "<b>" + u'\U0001F4E3' + " Upcoming</b>" + " <i>@" + _time + "</i>" + "\n" + _event + "\n" + "(Forecast: " + _forecast + ", Previous: " + _previous + ")" + "\n\n"

    print("Passage: [" + passage + "]")
    return passage

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
        print(_converted_date)
        print(_dayname)
        print(_time + "-" + _event)        
        if (_converted_date.date() >= now.date()):
            passage = passage + "<b>" + _date + " (" + _dayname + ")" + "</b>" + " <i>@" + _time + "</i>" + "\n" + _event + "\n\n"
    
    if (passage == ""):
        passage = "No event for today."
    
    print("Passage: [" + passage + "]")
    return passage

def main(args):

    if (len(args) > 1):

        if (args[1] == "gen_daily"):
            passage = "Major Market Events for today" + "\n\n" + get_fx_calendar()
            bot_sender.broadcast_list(passage, "telegram-chart")
        elif (args[1] == "gen_hourly"):
            passage = get_fx_calendar_notice()

            if (passage):
                passage = u'\U0001F514' + "Market Events Alerts" + u'\U0001F514' +  "\n\n" + passage
                bot_sender.broadcast_list(passage, "telegram-fx")
    else:
        print("OPTS: gen_daily | gen_hourly")
 
if __name__ == "__main__":
    main(sys.argv)        
        

