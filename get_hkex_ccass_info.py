from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser

from selenium import webdriver

config = configparser.ConfigParser()
config.read('config.properties')

def get_latest_ccass_info(code, number):

    DEL = "\n\n"
    EL = "\n"
    passage = ""

    if (is_number(code) and is_number(number)):
        print("Code to Quote: [" + code + "]")
        print("Number to Grab: [" + str(number) + "]")           
    else:
        return "<i>Usage:</i> " + "/qC" + "[StockCode] (e.g. " + "/qC2899" + ")"   
    
    browser = webdriver.Chrome('C:\project\common\chromedriver.exe')
    browser.get(r'http://www.hkexnews.hk/sdw/search/searchsdw_c.aspx')

    elemCode = browser.find_element_by_name('txtStockCode')
    elemCode.send_keys(code)
    
    elemSearch = browser.find_element_by_name('btnSearch')
    elemSearch.click()
    
    # Detect if there is any alert
    try:
        alert = browser.switch_to_alert()
        error = alert.text
        alert.accept()
        print("alert accepted")
        browser.close()
        return  u'\U000026D4' + " " + error
    except:
        print("no alert")
    
    html = browser.page_source
    
    browser.close()

    #print("Result: [" + str(html.encode("utf-8")) + "]")  
    
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', id="pnlResultHeader")
    tables = div.findAll('table')
    title = ""
    
    # Stock code exists
    if (tables[3]):
        
        cols = tables[3].findAll('td')
        title = cols[3].text.strip("/r/n").strip() + " (" + cols[1].text.strip("/r/n").strip() + ")"

        ctable = soup.find('table', id="participantShareholdingList")        
        rows = ctable.findAll('tr')[3:3+number]
        
        #print(len(rows))
        
        count = 1
        
        for row in rows:
            cols = row.findAll('td')
              
            pid = cols[0].text.strip("/r/n").strip()
            pname = cols[1].text.strip("/r/n").strip()
            pshares = cols[3].text.strip("/r/n").strip()
            ppercentage = cols[4].text.strip("/r/n").strip()
            
            #passage = passage + str(count) + ": " + pid + " - " + pname + " (" + pshares + ", " + ppercentage + ")" + EL
            passage = passage + str(count) + ". " + pname + "" + EL + "Shares: " + pshares + " (" + ppercentage + ")" + DEL
            
            count = count + 1
    
    if (not passage):
        passage =  u'\U000026D4' + "No matching info is found!"
    else:
        passage = "<i>Top 10 CCASS for " + title + "</i>" + DEL + passage
    
    return passage   
    
def main():

    print(get_latest_ccass_info("939", 5).encode("utf-8"))
    
    print(get_latest_ccass_info("99999", 5).encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



