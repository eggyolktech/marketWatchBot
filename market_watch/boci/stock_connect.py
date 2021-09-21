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
 
def get_week_high():

   
    url = "https://www.bocifp.com/tc/ah/stock-connect"
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    chartTable = soup.find('table', {'class': 'chart_table'})
    rows = chartTable.find_all("tr")[1:]

    for row in rows:

        cols = row.find_all('td')
        code = cols[0].text.strip()
        name = cols[1].text.strip()
        buy = cols[3].text.strip()
        sell = cols[4].text.strip()
        chg = cols[8].text.strip()

        passage = passage + ("/qq%s /qd%s (%s)" % (code, code, name)) + EL
        passage = passage + ("買入:%s / 賣出:%s (%s)" % (buy, sell, chg)) + DEL

    if passage:
        passage = u'\U0001F514' + " 十五大港股通成交活躍股" + DEL + passage

    return passage
    
def main():

    passage = get_week_high()

    print(passage)
    bot_sender.broadcast(passage, False)
   
if __name__ == "__main__":
    main()                
              



