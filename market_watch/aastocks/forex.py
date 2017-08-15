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


def get_forex():

    DEL = "\n\n"
    EL = "\n"

    url = "http://www.aastocks.com/tc/forex/quote/worldcurrency.aspx?cate=6&sort=1&order=0"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    fxTable = soup.find("table", {"class": "invest_table"})

    passage = "<b>環球外匯走勢</b>" + DEL

    passage = passage + "DXY: " + live_rate.get_dxy_live_rate() + EL

    for tr in fxTable.findAll("tr")[2:]:

        name = tr.findAll("td")[0].text.strip()
        last = tr.findAll("td")[1].text.strip()
        change = tr.findAll("td")[2].text.strip()
        change = change.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
        change_pct = tr.findAll("td")[3].text.strip()
        change_pct = change_pct.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
        hlrange = tr.findAll("td")[4].text.strip()

        passage = passage + name + ": " + last + " " + change + "(" + change_pct + ")" + EL
   
    if (not passage):
        passage = "No fx rates found."
    
    return passage   
    
def main():

    print(get_forex())
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



