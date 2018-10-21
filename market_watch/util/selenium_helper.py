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

def get_content(url, waittime=0):

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

    print("URL: [" + url + "]")

    browser.get(url)

    for num in range(0, waittime):

        print("Start dummy pass %s..." % (num+1)) 
        
        try:
            browser.implicitly_wait(3) # seconds
            myDynamicElement = browser.find_element_by_id("dummyid")
        except:
            pass

    html = browser.page_source
    browser.close()
    #print(html)
    return html 

def main():
    
    html = get_content('https://m.weibo.cn/p/1005056735409154', 3)
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



