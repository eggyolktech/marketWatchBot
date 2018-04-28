#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse as urlparse
import requests
import re
from datetime import datetime

from market_watch.telegram import bot_sender
from market_watch.db import profit_warning_db
from market_watch.etnet import result_announcement
from hickory.crawler.aastocks import stock_info

DEL = "\n\n"
EL = "\n"
 
def get_latest_reports(reporttype=9):

   
    if (reporttype == 9): 
        url = "http://news.sina.com.tw/cobrand/cnyes/"
    else:
        print("Invalid Report Type")
        return

    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passages = [] 
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    divTag = soup.find("div", {"class": "listcont"})

    liList = divTag.find_all("li")

    for tag in liList:
        a = tag.find('a')
        c = tag.find('cite')
        ctime = c.text.split("】")[1]
        aURL = a['href']
        aURL = "http://news.sina.com.tw" + aURL
        
        newsid = aURL.split("/")[-1].replace(".html","")
        print(str(a.text.strip()) + " - " + newsid)
        
        if (not profit_warning_db.add_warning(ctime, newsid, str(reporttype))):
            print("Logtime already reported before: [" + tag.text.strip() + " - " + newsid + "]")
            break
          
        passage = "<a href='" + aURL + "' target='_blank'>" + a.text + "</a> (" + c.text.split("】")[1] + ")" + EL
        passages.append(passage)   

    return passages 
    
def main():

    # us stock news
    for report in get_latest_reports():
        print(report)
        bot_sender.broadcast_list(report, "telegram-notice")
        #bot_sender.broadcast(report)

if __name__ == "__main__":
    main()                
              



