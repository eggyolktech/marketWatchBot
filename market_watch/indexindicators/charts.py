#!/usr/bin/python


from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
from market_watch.telegram import bot_sender

DEL = "\n\n"
EL = "\n"
CL = ":"
URL = "http://www.aastocks.com"

def get_breadth(chart_type):

    url = "http://www.indexindicators.com/charts/%s" % (chart_type)
     
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    img = soup.find("img", {"class": "chart-img"})

    if (img):
        return img['src']
    else:
        return None

    
    return passage   
 
def main():

    for ct in ["sp500-vs-sp500-stocks-above-20d-sma-params-x-x-x-x",
               "djia-vs-djia-stocks-above-20d-sma-params-x-x-x-x",
               "nasdaq100-vs-nasdaq100-stocks-above-20d-sma-params-x-x-x-x",
              ]:
        url = get_breadth(ct)
        if (url):
            bot_sender.send_remote_image(url, "telegram-twitter")
    
    
if __name__ == "__main__":
    main()                
              



