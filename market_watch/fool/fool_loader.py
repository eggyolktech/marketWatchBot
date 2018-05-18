#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from market_watch.telegram import bot_sender

DEL = "\n\n"

def get_analysis(code):
    
    url = "https://www.fool.com/quote/%s" % code.strip()

    print("Url: [" + url + "]")
    passage = ""

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text 
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
   
   
    divs = soup.findAll("div", {"class": "article-container"})
    links = soup.findAll("a", {"a": "article-link"})
    ftitle = "Latest updates on %s from Fool.com" % code.upper().strip()
    count = 0

    print("\n" + str(datetime.fromtimestamp(time.mktime(gmtime()))))
       	
    for div in divs:
    
        link = div.find("a", {"class": "article-link"})
        meta = div.find("span", {"class": "article-meta"})
        updated = meta.text.split("•")[0].strip()
        
        passage = passage + "<a href='"+ link['href'] + "'>" + link.text + "</a> (" + updated + ")" + DEL
        count += 1

    print("Total # of links processed: %s" % (count))
   
    if (passage):
        passage = u'\U000024C2' + " " + ftitle + DEL + passage
    else:
        passage = "No Fool.com analysis found for %s" % code.strip()
 
    #print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    passage = get_analysis("BABA")
    print(passage)
    #print(get_analysis("BA1BA"))


if __name__ == "__main__":
    main()        
        

