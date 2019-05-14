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

   
    url = "http://www.etnet.com.hk/www/tc/stocks/breakrecord.php?subtype=52wkhigh"
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    div = soup.find_all("div", {"class": "DivFigureContent"})[0]
    rows = div.find_all("tr")[1:]

    for row in rows:

        cols = row.find_all('td')
        code = cols[1].text.strip()
        name = cols[2].text.strip()
        close = cols[4].text.strip()
        chg = cols[5].text.strip()
        chgp = cols[6].text.strip()
        turnover = cols[9].text.strip()
        ind = cols[11].text.strip()

        if not ind:
            ind = "ETF"
        
        passage = passage + ("/qd%s %s (%s)" % (code, name, ind)) + EL
        passage = passage + ("Close: %s (%s/%s), %s" % (close, chg, chgp, turnover)) + DEL

    if passage:
        passage = u'\U0001F514' + " 創52周新高港股名單" + DEL + passage

    return passage
    
def main():

    passage = get_week_high()

    print(passage)
    bot_sender.broadcast(passage, False)
   
if __name__ == "__main__":
    main()                
              



