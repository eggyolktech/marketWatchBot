#!/usr/bin/python

# imdb process import
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
import time
import sys
from datetime import date
from datetime import datetime


def get_aastocks_industry():

    url = "http://services1.aastocks.com/web/cjsh/IndustrySection.aspx?CJSHLanguage=Eng"

    #print("Url: [" + url + "]")
    
    r = requests.get(url, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, 'html5lib')
    
    for option in soup.find_all('option', {}):
        
        print('\n============== Value: {}, Industry: {}'.format(option['value'], option.text))
        
        if (option['value'] != "0"):
            list_url = "http://services1.aastocks.com/web/cjsh/IndustrySection.aspx?CJSHLanguage=Eng&symbol=&industry=" + option['value']
            #print ("List URL: [" + list_url + "]")
            
            r = requests.get(list_url, timeout=10)
            html = r.text
            soup2 = BeautifulSoup(html, 'html5lib')
            
            for tr in soup2.find_all('tr', {'class': ['DR','ADR']}):
                print('Symbol: {}, Desp: {}'.format(tr.select('td')[0].text, tr.select('td')[1].text))
                
            time.sleep(5)
      
get_aastocks_industry()



