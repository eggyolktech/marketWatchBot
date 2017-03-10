# imdb process import
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser
#config = ConfigParser.RawConfigParser()
#config.read('ConfigFile.properties')


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
        
    url = "https://www.dailyfx.com/calendar?previous=true&week=" + str(year) + "/" +  start_of_week + "&currentweek=currentweek&tz=+08:00&currency=&importance=high"

    print("Url: [" + url + "]")
    
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    #table = soup.find('table', {'id': 'daily-cal4'})
    
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
 
def send_to_tg_chatroom(passage): 

    bot_id = "193192163:AAGC4RFnLmU7uJSbrJFPz1y36202O_NJcDU"
    result = urllib.request.urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": -172861420, "text": passage }).encode("utf-8")).read()
    print(result) 
  
# sync top 100 list
passage = get_fx_calendar()

#print(passage)

# Send a message to a chat room (chat room ID retrieved from getUpdates)
send_to_tg_chatroom(passage)
