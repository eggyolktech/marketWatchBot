#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import time
import re
import requests
from bs4 import BeautifulSoup

DEL = "\n\n"

def get_sec_list(symbol):

    symbol = symbol.strip().upper()

    url = "http://quantumonline.com/ParentCoSearch.cfm?tickersymbol=%s" % symbol

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text.replace("<p>","")
    #print(html)
    soup = BeautifulSoup(html, "html5lib")    
    rows = soup.find("ul").find("table").find("tbody").findAll("tr")
    
    passage = ""

    
    for row in rows[1:]:
        
        cols = row.findAll("td")
        
        if (cols):
        
            tsymbol = cols[0].text.strip()
            thref = cols[0].find("a")['href']
            tdesc = cols[1].text.strip()
            texchange = cols[2].text.strip()
        
            if (not "*" in tsymbol) and (not symbol == tsymbol):
                msgtmpl = "<a href='http://quantumonline.com/%s'>%s</a> /qq%s\n - %s (%s)"
                passage = passage + (msgtmpl % (thref, tsymbol, tsymbol, tdesc , texchange)) + DEL
    
    if (passage):
        passage = u'\U0001F514' + " Related Securities for Parent Company: %s" % symbol + DEL + passage
        return passage
    else:
        return "No securities found"

def main():

    list = ["ssw", "ge", "tencnt", "jpm", "tesla", "amzn"]
    list = ["ssw"]
    for ticker in list:
        print(get_sec_list(ticker))

if __name__ == "__main__":
    main()        
        

