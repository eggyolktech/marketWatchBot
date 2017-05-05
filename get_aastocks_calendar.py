from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser

from classes.AastocksConstants import *

config = configparser.ConfigParser()
config.read('config.properties')


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
 
def send_to_tg_chatroom(passage): 

    chat_list = config.items("telegram-chat")
    bot_send_url = config.get("telegram","bot-send-url")
    
    for key, chat_id in chat_list:
        print("Chat to send: " + key + " => " + chat_id);

        result = urllib.request.urlopen(bot_send_url, urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": chat_id, "text": passage }).encode("utf-8")).read()
        
        print(result)

def main():
    # sync top 100 list
    passage = get_aastocks_calendar()

    # Send a message to a chat room (chat room ID retrieved from getUpdates)
    send_to_tg_chatroom(passage)

if __name__ == "__main__":
    main()        
        

