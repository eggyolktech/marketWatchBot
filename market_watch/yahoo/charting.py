#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

def get_tse_chart(code, period):

    url_dict = {"m": "https://chart.yahoo.co.jp/?code=%s.T&tm=1d&vip=off", "h": "https://chart.yahoo.co.jp/?code=%s.T&tm=5d&vip=off" ,"d": "https://chart.yahoo.co.jp/?code=%s.T&tm=6m&type=c&log=off&size=n&over=s,e25,e75,v&add=m,r,ss&comp=" ,"w": "https://chart.yahoo.co.jp/?code=%s.T&tm=2y&type=c&log=off&size=n&over=s,v,e130,e260,e65&add=m,r&comp=" ,"M": "https://chart.yahoo.co.jp/?code=%s.T&tm=ay&type=c&log=off&size=n&over=s,v,e130,e260,e65&add=&comp="}
    url = url_dict[period] % (code[:4])    
    return url

def is_tse_code(code):
    
    pattern = r"\d{4}[jJ]$"
    if (re.match(pattern, code)):
        return True
    else:
        return False

def main():

    for code in ["4911J","4922j"]:
        print(get_tse_chart(code, "d"))

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              
