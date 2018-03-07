#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

def get_latest_news_by_code(code, number):

    DEL = "\n\n"
    EL = "\n"
    URL = "http://www.aastocks.com"

    if (is_number(code) and is_number(number)):
        print("Code to Quote: [" + code + "]")
        print("Number to Grab: [" + str(number) + "]")           
    else:
        return "<i>Usage:</i> " + "/qn" + "[StockCode] (e.g. " + "/qn2899" + ")"   
    
    url = "http://www.aastocks.com/tc/stocks/news/aafn-company-news/%s/0/all/1/1" % (code)
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    
    passage = ""
    count = 0

    for a in soup.findAll('a', id=re.compile("^cp_ucAAFNSearch_repNews")):
        #print(link)
        t = a.parent.find_next_sibling("div")
        aURL = a['href']
        aTitle = a['title']
        if aURL.startswith("/"):
             aURL = "http://www.aastocks.com" + aURL

        if not any(x in aTitle for x in ["窩輪", "牛熊證", "輪證"]):
            count = count + 1
            passage = passage + DEL + "<a href='" + aURL + "' target='_blank'>" + a['title'] + "</a> (" + t.getText()[-11:] + ")"

        if count >= number:
            break

   if (not passage):
        passage = "Oops...something wrong for the new feed!"
    else:
        passage = "<i>Latest News Feed for " + code + ".HK</i>" + passage
    
    return passage   
    
def main():

    print(get_latest_news_by_code("939", 5).encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



