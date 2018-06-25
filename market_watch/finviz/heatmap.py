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

def get_map():

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

    url = "https://finviz.com/map.ashx?t=sec"    
    print("URL: [" + url + "]")

    browser.get(url)
   
    try:
        myDynamicElement = browser.find_element_by_id("share-map")
        myDynamicElement.click()
    except:
        pass   
    
    print("Start dummy pass...") 
    try:
        browser.implicitly_wait(3) # seconds
        myDynamicElement = browser.find_element_by_id("dummyid")
    except:
        pass

    print("Start dummy pass 2...") 
    try:
        browser.implicitly_wait(3) # seconds
        myDynamicElement = browser.find_element_by_id("dummyid")
    except:
        pass

    print("Start dummy pass 3...") 
    try:
        browser.implicitly_wait(3) # seconds
        myDynamicElement = browser.find_element_by_id("dummyid")
    except:
        pass
   
    try:
        browser.implicitly_wait(5) # seconds
        alert = browser.switch_to_alert()
        error = alert.text
        alert.accept()
        print("alert accepted")
        browser.close()
    except:
        print("no alert")
    
    html = browser.page_source
    browser.close()
    #print(html)
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
    furl = "https://finviz.com/chart.ashx?t=%s&ta=1&p=d&s=l" % code

    #message = "<a href='%s'>Quick Chart for %s</a> (<a href='%s'>Profile</a>)" % (furl, code.upper(), purl)
    return furl
    
def main():
    
    #print(get_chart("baba"))    

    url = None
    url = get_map()
    if (url):
        bot_sender.send_remote_image(url, "telegram-twitter")
        bot_sender.send_remote_image(url, "telegram-twitter-zerohedge")
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



