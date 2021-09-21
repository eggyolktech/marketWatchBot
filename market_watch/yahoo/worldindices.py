#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

EL = "\n"
DEL = "\n\n"

def get_indices():

    url = "https://hk.finance.yahoo.com/world-indices/"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    root = "https://hk.finance.yahoo.com"
 
    r = requests.get(url, headers=headers)
    html = r.text 
    #print(html)
    soup = BeautifulSoup(html, "html.parser")

    section = soup.find("section", {"id": "yfin-list"})
    #print(section)
    
    rows = section.find("table").find("tbody").findAll("tr")

    passage = "<b>" + "世界指數" + "</b>" + DEL

    for row in rows:
        cols = row.findAll("td")
        link = root + cols[0].find("a")['href']
        index = cols[1].text
        close = cols[2].text
        change = cols[3].text
        change = change.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
        changepct = cols[4].text
        changepct = changepct.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')

        passage = passage + ("<a href='%s'>%s</a> : %s (%s / %s)" % (link, index, close, change, changepct)) + EL
        
    return passage 

def main():

    print(get_indices())

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              
