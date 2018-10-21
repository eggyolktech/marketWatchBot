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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from market_watch.redis import redis_pool

def refresh(code):

    DEL = "\n\n"
    EL = "\n"
    
    if (os.name == 'nt'):
        options = Options()  
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_argument('--disable-gpu')
        #options.add_argument('--headless')
        
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"  #  complete
        browser = webdriver.Chrome(desired_capabilities=caps, executable_path="C:\Wares\chromedriver.exe", chrome_options=options)  
    else:

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        #dcap["pageLoadStrategy"] = "none"  #  complete
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
            )
        browser = webdriver.PhantomJS(desired_capabilities=dcap)

    url = "http://stockcharts.com/h-sc/ui"    
    print("URL: [" + url + "]")

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

    print("Browser get...")
    browser.get(url)
    print("Browser get complete...")
    
    try:
        #print(str(browser.find_element_by_id("symbol")))
        
        browser.find_element_by_xpath("//input[@id='symbol']").send_keys(code)
        browser.find_element_by_xpath("//select[@name='overType_2']/option[text()='Pivot Points']").click()
        browser.find_element_by_xpath("//input[@id='submitButton']").click()
        #wform.find_element_by_id("").click()        
    except:
        traceback.print_exc()
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
    #browser.close()
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img", {"class": "chartimg"})
    
    if(img and img['src']):
        token = img['src'].split("&i=")[1]
        redis_pool.setV("STOCKCHARTS:TOKEN", token)
        print("Token: [%s]" % token)
    else:
        print("No Token is found!")
    
    #/c-sc/sc?s=BABA&p=D&b=5&g=0&i=t80798412901&r=1530199590041
    return

def main():

    refresh("baba")
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              




