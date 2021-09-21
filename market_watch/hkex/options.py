#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import re
import os
from datetime import date
from datetime import datetime
from selenium import webdriver

def get_options_list():

    if (os.name == 'nt'):
        browser = webdriver.Chrome('C:\project\common\chromedriver.exe')
    else:
        browser = webdriver.PhantomJS() 
 
    browser.get(r'https://www.hkex.com.hk/Products/Listed-Derivatives/Single-Stock/Stock-Options?sc_lang=zh-HK')

    html = browser.page_source
    browser.close()

    #print("Result: [" + str(html.encode("utf-8")) + "]")  
    
    soup = BeautifulSoup(html, "html.parser")
    masterDiv = soup.find('div', {'class': 'common_panel_content'})
     
    tbody = masterDiv.find('tbody')

    options_list = []

    for tr in tbody.find_all('tr'):
        cols = tr.find_all('td')
        
        stock = (cols[1].text.strip(), cols[2].text.strip())
        options_list.append(stock)
 
    return options_list

def main():

    print(get_options_list())
 
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



