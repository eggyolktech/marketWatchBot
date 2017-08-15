#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
from market_watch.fxcm import live_rate


def get_commodities():

    DEL = "\n\n"
    EL = "\n"

    url = "http://m.stockq.org/commodity.php"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    r.encoding = "UTF-8"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    cTable = soup.find("table", {"class": "marketdatatable"})

    passage = "<b>商品價格 (Stockq)</b>" + DEL

    for tr in cTable.findAll("tr", {'class':['row1', 'row2']}):

        name = tr.findAll("td")[0].text.strip()
        last = tr.findAll("td")[1].text.strip()
        change = tr.findAll("td")[2].text.strip()
        if ("-" in change):
            change = change.replace("-", u'\U0001F53B')
        else:
            change = u'\U0001F332' + change
        change_pct = tr.findAll("td")[3].text.strip()
        if ("-" in change_pct):
            change_pct = change_pct.replace("-", u'\U0001F53B')
        else:
            change_pct = u'\U0001F332' + change_pct

        passage = passage + name + ": " + last + " " + change + "(" + change_pct + ")" + EL
   
    if (not passage):
        passage = "No commodity rates found."
    
    return passage   
    
def main():

    print(get_commodities())
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



