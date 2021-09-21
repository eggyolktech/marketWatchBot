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
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from market_watch.telegram import bot_sender

import traceback
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def get_map(cat="sec"):

    DEL = "\n\n"
    EL = "\n"

    if (os.name == 'nt'):
        options = Options()  
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path="C:\Wares\chromedriver.exe", chrome_options=options)  
    else:
        browser = webdriver.PhantomJS() 

    url = "https://finviz.com/map.ashx?t=%s" % cat    
    print("URL: [" + url + "]")

    browser.get(url)
   
    try:
        myDynamicElement = browser.find_element_by_id("share-map")
        myDynamicElement.click()
    except:
        traceback.print_exc()
        pass   


    for i in range(4):
        print("Start dummy pass %s..." % i) 

        try:
            browser.implicitly_wait(3) # seconds
            myDynamicElement = browser.find_element_by_id("dummyid")
        except:
            traceback.print_exc()
            pass

    try:
        browser.implicitly_wait(5) # seconds
        alert = browser.switch_to_alert()
        error = alert.text
        alert.accept()
        print("alert accepted")
        browser.close()
    except:
        traceback.print_exc()
        print("no alert")
    
    html = browser.page_source
    browser.close()
    print("*" * 100)
    print(html)
    print("*" * 100)
    soup = BeautifulSoup(html, "html.parser")
    divOverlay = soup.find("div", {"class": "overlay"})
    #print(divOverlay)
    imgurl = divOverlay.find("img")['src']
    return imgurl

def get_charts(code, params):

    urls = []

    if (not is_number(code)):
        urls.append(get_chart(code))

    for p in params:
        if (not is_number(p)):
            urls.append(get_chart(p))
    print(urls)
    return urls

def get_chart(code):

    purl = "https://finviz.com/quote.ashx?t=%s" % code
    furl = "https://finviz.com/chart.ashx?t=%s&ta=1&p=d&s=l&ts=%s" % (code, current_milli_time())

    #message = "<a href='%s'>Quick Chart for %s</a> (<a href='%s'>Profile</a>)" % (furl, code.upper(), purl)
    return furl
    
def main():
    
    #print(get_chart("baba"))    
    print(get_map('geo'))
    return

    urls = []

    for cat in ('sec', 'geo', 'etf'):
        
        try:
            urls.append(get_map(cat))
        except:
            print("Error in getting cat %s" % cat)

    print(urls)

    for url in urls:
        bot_sender.send_remote_image(url, "telegram-twitter")
        bot_sender.send_remote_image(url, "telegram-zerohedge")
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



