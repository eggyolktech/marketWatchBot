#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import resource
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

def get_pricehist(name):

    DEL = "\n\n"
    EL = "\n"

    if (os.name == 'nt'):
        options = Options()  
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path="C:\Wares\chromedriver.exe", chrome_options=options)  
    else:
        options = Options()
        #options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        #options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        print(options)
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-gpu')
        #options.add_argument('--disable-extensions')
        #options.add_argument('--headless')
        #options.add_argument('--disable-dev-shm-usage')
        #driver_path = "/usr/lib/chromium-browser/chromedriver"
        
        capabilities = {
            'browserName': 'chrome',
            'chromeOptions':  {
                'useAutomationExtension': False,
                'args': ['--headless', '--no-sandbox']
            }
        }    

        browser = webdriver.Chrome(desired_capabilities=capabilities)

        #browser = webdriver.Chrome(executable_path="/usr/lib/chromedriver", chrome_options=options, service_args=["--verbose", "--log-path=qc1.log"])
        #browser = webdriver.PhantomJS() 

    if (name.strip() == ""):
        return "Usage: /qt[search name] e.g. /qt德寶"

    url = "https://data.28hse.com/"    
    print("URL: [" + url + "]")

    browser.get(url)
    
    selectb = browser.find_elements_by_class_name("data-keywords-wrapper");
    selectb[0].click()
    
    input = browser.find_elements_by_class_name("select2-search__field");
    #print(input)
    input[0].send_keys(name)

    try:
        browser.implicitly_wait(3) # seconds
        myDynamicElement = browser.find_element_by_id("dummyid")
    except:
        pass 
    
    input[0].send_keys(Keys.ENTER)

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
        #browser.close()
    except:
        print("no alert")

    furl = browser.current_url    
    html = browser.page_source
    browser.close()
    #print(html)
    soup = BeautifulSoup(html, "html.parser")    

    txnhead = soup.find("div", {"class": "data-txn"})

    if (txnhead):
        return "沒有找到相符的資料: %s" % name

    info = soup.find("div", {"class": "estate-info"})

    pname = name
    if (info):
        pname = info.findAll("td")[1].text
        print(pname) 
    
    tbody = soup.find("tbody", {"class": "data-txn-table-body"})
    
    if (tbody):
        rows = tbody.findAll("tr")
    else:
        return "No result was found"
    
    passage = ""
    
    for row in rows[:10]:
        cols = row.findAll("td")
       
        if len(cols) == 1:
            return "暫無成交紀錄: %s" % pname
 
        date = cols[0].text.strip()
        price = cols[1].text.strip()
        change = cols[2].text.strip() 
        
        if (cols[2].find("span")):
            span = cols[2].find("span")
            #print(span['class'])
            if (span.has_attr('class')):
                if span['class'] == ['data-txn-winloss-loss']:
                    change = "-" + change
                elif span['class'] == ['data-txn-winloss-win']:
                    change = "+" + change

        size = cols[3].text.strip()
        unitprice = cols[4].text.strip()
        address = cols[5].text.strip()
        contract = cols[6].text.strip()
        
        passage = passage + ("<i>%s</i> - %s - %s (%s)" + EL + "%s (%s) %s") % (date, address, price, change, size, unitprice, contract) + DEL
        
    if (passage):
        passage = u'\U0001F514' + " Prices History for: %s" % (pname) + DEL + passage + furl
 
    return passage

def urlify(s):

     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s\/\-\+\.]", '', s)

     # Replace all runs of whitespace with a single dash
     s = re.sub(r"\s+", '', s)
     s = re.sub(r"\/", '|', s)

     return s
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def main():

    # Set resource limit
    rsrc = resource.RLIMIT_DATA
    soft, hard = resource.getrlimit(rsrc)
    print('Soft limit start as :' + str(soft))

    resource.setrlimit(rsrc, (100 * 1024, hard))
    soft, hard = resource.getrlimit(rsrc)

    print('Soft limit start as :' + str(soft))

    list = ["淘大", "駿發", "喜"]
    list = ["", "天匯"]
    list = ["軒大屋","黃埔","天鑄"]
    for ticker in list:
        print(get_pricehist(ticker))

if __name__ == "__main__":
    main()        
        



