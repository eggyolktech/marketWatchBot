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
from market_watch.db import profit_warning_db

DEL = "\n\n"
EL = "\n"

def get_result_calendar(code):

    url = "http://www.aastocks.com/tc/stocks/market/calendar.aspx?type=1&s=0&searchsymbol=%s" % code

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    passage = ""
    now = datetime.now()

    print("Timestamp now: [" + str(now) + "]")
    rows = soup.find("table", {"class": "CalendarResultTable"}).find_all("tr")

    if (len(rows) >= 3):
        cols = rows[1].findAll("td")
        rdate = cols[0].text.strip()
        rcode = cols[1].text.strip()
        rdetail = cols[3].text.strip()

        passage = "<b>" + rcode + "</b>" + EL + rdate + " - " + rdetail

    else:
        passage = rows[1].text.strip()

    return passage



def get_latest_result_announcement():

    url = "http://www.aastocks.com/tc/stocks/news/aafn/result-announcement"

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    passages = []
    passage = ""
    now = datetime.now()

    print("Timestamp now: [" + str(now) + "]")
    divs = soup.find_all("div", {"class": "content_box"})

    for div in divs:
        link = div.find("a", {"class": "h6"},  href=re.compile("/tc/stocks/news/aafn-content/"))
        divTime = div.find("div", {"class":"newstime2"})
        if (link and divTime and "業績" in link.text):

            aURL = "http://www.aastocks.com" + link["href"]
            aNewsID = link["href"].split("/")[5]
            aDate = divTime.text
            print(aNewsID)
            
            if (not profit_warning_db.add_warning(aDate, aNewsID, 3)):
                print("Logtime already reported before: [" + aDate + " - " + aNewsID + "]")
                break

            passage = "<a href='" + aURL + "' target='_blank'>" + link.text + "</a> (" + aDate + ")"
            passages.append(passage)

    return passages

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
   
    #print(get_result_calendar("700"))
    #print(get_result_calendar("3993"))
 
    #for passage in get_latest_result_announcement():
    #    print(passage)

if __name__ == "__main__":
    main()        
        

