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

def get_sec_list(symbol):

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

    url = "https://www.bondsupermart.com/main/general-search"    
    print("URL: [" + url + "]")

    browser.get(url)
    
    input = browser.find_element_by_id("search-key")
    input.send_keys(symbol)
    input.send_keys(u'\ue007')

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
    table = soup.find("table", {"id": "bond-info-table"})
    
    if (table):
        rows = table.find("tbody").findAll("tr")
    else:
        return "No result was found"
    
    passage = ""
    issuer = ""
    last_issuer = ""
    issuerRating = ""
    
    for row in rows[:8]:
        cols = row.findAll("td")
        issuer = cols[0].find_all(text=True, recursive=False)[0].strip()
        secName = cols[0].find('a').text.strip()
        secLink = 'https://www.bondsupermart.com' + cols[0].find('a')['href']
        lotSize = cols[2].text.strip()
        bondRating = urlify(cols[3].text.strip())
        issuerRating = urlify(cols[4].text.strip())
        yearsLeft = cols[5].text.strip()
        coupon = cols[6].text.strip()
        askPrice = cols[7].text.strip()
        BidYTM = cols[8].text.strip()
        AskYTM = cols[9].text.strip()
        
        if (not last_issuer == issuer):
            passage = passage + "Issuer: %s\nIssuer Rating: %s (S&P|Fitch)" % (issuer, issuerRating) + DEL 
        passage = passage + "<a href='%s'>%s</a>\nLotSize: $%s, Rating(S&P|Fitch): %s\nYearsToMat: %s, Cpn: %s%%\nAskPx: $%s\nBidYTM: %s%%, AskYTM: %s%%" % (secLink, secName, lotSize, bondRating, yearsLeft, coupon, askPrice, BidYTM, AskYTM) + DEL
        
        last_issuer = issuer
        
    if (passage):
        passage = u'\U0001F514' + " Related Securities for Symbol: %s" % (symbol) + DEL + passage
 
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

    list = ["ssw", "ge", "tencnt", "jpm", "tesla", "amzn"]
    list = ["dsdadsa", "ge", "amzn"]
    for ticker in list:
        print(get_sec_list(ticker))

if __name__ == "__main__":
    main()        
        



