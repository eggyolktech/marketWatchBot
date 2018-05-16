#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from market_watch.redis import redis_pool

DEL = "\n\n"
KEY = "OPTIONS:List"

def get_ust_yield():

    url = "http://money.cnn.com/data/bonds/"

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
   
    rows = soup.find("table", {"id": "treasuryYields_datatable"}).find("tbody").findAll("tr")
    updatetime = soup.find("div", {"class": "wsod_dateBlock"}).text
    
    results = []
    passage = ""
    
    
    
    for row in rows:
        cols = row.findAll("td")
        passage = passage + "<b>%s</b> - Last Yield: %s, Previous Yield: %s" % (cols[0].text, cols[1].text, cols[2].text) + DEL
    
    if (passage):
        passage = passage + updatetime
        passage = u'\U0001F514' + " Latest U.S. Treasury Yields" + DEL + passage
        return [passage, "http://markets.money.cnn.com/bondsandrates/modules/chart.asp?type=yield"]
    else:
        return []

def main():

    print(get_ust_yield())

if __name__ == "__main__":
    main()        
        

