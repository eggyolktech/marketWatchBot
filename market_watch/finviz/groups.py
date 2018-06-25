#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
import os
from datetime import date
from datetime import datetime
from selenium import webdriver
from market_watch.telegram import bot_sender

def get_groups_chart():

    DEL = "\n\n"
    EL = "\n"

    url = "https://finviz.com/groups.ashx?g=sector&v=210&o=name"    
    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 

    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    
    images = soup.find_all("img", src=re.compile("^grp_image.ashx"))
    urls = []
    
    for img in images[1:]:
        urls.append("https://finviz.com/%s" % img['src'])
    
    return urls

def main():
    
    urls = None
    urls = get_groups_chart()
    if (urls):
        for url in urls:
            bot_sender.send_remote_image(url, "telegram-chat-test")
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



