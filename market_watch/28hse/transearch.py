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
        browser = webdriver.PhantomJS() 

    url = "https://data.28hse.com/"    
    print("URL: [" + url + "]")

    browser.get(url)
    
    selectb = browser.find_elements_by_class_name("data-keywords-wrapper");
    selectb[0].click()
    
    input = browser.find_elements_by_class_name("select2-search__field");
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
    
    html = browser.page_source
    browser.close()
    #print(html)
    soup = BeautifulSoup(html, "html.parser")    
    
    tbody = soup.find("tbody", {"class": "data-txn-table-body"})
    
    if (tbody):
        rows = tbody.findAll("tr")
    else:
        return "No result was found"
    
    passage = ""
    
    for row in rows[:10]:
        cols = row.findAll("td")
        
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
        passage = u'\U0001F514' + " Prices History for Search Name: %s" % (name) + DEL + passage
 
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

    list = ["淘大", "駿發", "喜"]
    list = ["淘大", "駿發", "天匯"]
    for ticker in list:
        print(get_pricehist(ticker))

if __name__ == "__main__":
    main()        
        



