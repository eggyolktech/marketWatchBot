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
from market_watch.redis import redis_pool

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

    token = redis_pool.getV("STOCKCHARTS:TOKEN").decode("utf-8")
    furl = "http://stockcharts.com/c-sc/sc?s=%s&p=D&b=5&g=0&i=%s" % (code.upper(), token)
    return furl
    
def main():
    
    #print(get_chart("baba"))    
    url = get_chart("MSFT")
    print(url)
    if (url):
        bot_sender.send_remote_image(url)
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



