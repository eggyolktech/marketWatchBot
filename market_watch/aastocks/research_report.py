#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import datetime

from market_watch.telegram import bot_sender

def get_latest_reports(period):

    DEL = "\n\n"
    EL = "\n"
 
    url = "http://www.aastocks.com/tc/stocks/news/aafn/research-report"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passages = [] 
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    for div in soup.findAll('div', ref=re.compile("^NOW")):
        a = div.find('a', {"class", "h6"})
        t = div.find('div', {"class", "newstime2"})
        
        # Check time difference match with monitoring period
        pdate = datetime.strptime(t.getText().strip(), "%Y/%m/%d %H:%M")
        pdiff = now - pdate
        pdiff_mins = (pdiff.days * 24 * 60) + (pdiff.seconds/60)
        print("[Post @" + t.getText() + " - " + str(pdiff_mins) + "mins old]")    
        
        if (pdiff_mins > period):
            print("Posts timestemps exceed monitoring period [" + str(period) + "mins], abort now.")
            break
    
        if a:
            aURL = a['href']
            aTitle = a['title']
            if aURL.startswith("/"):
                aURL = "http://www.aastocks.com" + aURL
                passage = "<a href='" + aURL + "' target='_blank'>" + a['title'] + "</a> (" + t.getText() + ")" 
                passages.append(passage)   

    return passages 
    
def main():

    for report in get_latest_reports(40):
        bot_sender.broadcast(report)
   
if __name__ == "__main__":
    main()                
              



