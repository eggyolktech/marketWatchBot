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

   
    url = "https://www.tradingview.com/markets/stocks-usa/highs-and-lows-ath/"
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    table = soup.find_all("table", {"class": "tv-screener-table"})
    rows = table[0].find("tbody").find_all("tr")

    for row in rows:

        cols = row.find_all('td')
        code = cols[0].find("a", {"class": "tv-screener__symbol"}).text.strip()
        name = cols[0].find("span", {"class": "tv-screener__description"}).text.strip()
        close = cols[1].text.strip()
        chg = cols[3].text.strip()
        chgp = cols[2].text.strip()
        turnover = cols[5].text.strip()
        mkt_cap = cols[6].text.strip()
        sector = cols[10].text.strip()

        passage = passage + ("/qv%s %s (%s)" % (code, name, sector)) + EL
        passage = passage + ("Close: $%s (%s/%s), %s" % (close, chg, chgp, turnover)) + DEL

    if passage:
        passage = u'\U0001F514' + "US Stock (All Time High)" + DEL + passage

    return passage
    
def main():

    passage = get_week_high()

    print(passage)
    bot_sender.broadcast(passage, False)
   
if __name__ == "__main__":
    main()                
              



