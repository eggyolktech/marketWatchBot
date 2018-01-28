#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
from selenium import webdriver

def get_commodities():

    DEL = "\n\n"
    EL = "\n"

    browser = webdriver.PhantomJS()

    url = "http://quote.eastmoney.com/center/futurelist.html#11_5_0?sortType=(Volume)&sortRule=-1"
    
    print("URL: [" + url + "]")

    browser.get(url)
   
    try:
        alert = browser.switch_to_alert()
        error = alert.text
        alert.accept()
        print("alert accepted")
        browser.close()
    except:
        print("no alert")
    

    #r = requests.get(url, headers=headers, timeout=10)
    #r.encoding = "gb2312"
    html = browser.page_source
    browser.close()
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
    cTables = soup.findAll("table", {"class": "table-data"})
    passage = "<b>商品價格 (Eastmoney Finance)</b>" + DEL

    for table in cTables:

        for tr in table.findAll("tr")[1:]:

            cols = tr.findAll("td")
            a = cols[2].find('a', href=True)
            href = a['href']
            name = "<a href='" + href + "' target='_blank'>" + cols[2].text + "</a>"
            last = cols[3].text
            change = cols[4].text
            per_change = cols[5].text
           
            if ("-" in change):
                change = change.replace("-", u'\U0001F53B')
                per_change = per_change.replace("-", u'\U0001F53B')
            else:
                change = u'\U0001F332' + change
                per_change = u'\U0001F332' + per_change

            passage = passage + name + ": " + last + " " + change + " (" + per_change + ")" + EL
   
    if (not passage):
        passage = "No commodity rates found."
    
    return passage   
    
def main():

    print(get_commodities())
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



