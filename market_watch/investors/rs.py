#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse as urlparse
import requests
import re
from datetime import datetime
import json
import sys

from market_watch.telegram import bot_sender
from market_watch.util import selenium_helper
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

DEL = "\n\n"
EL = "\n"

def rs_rating(code):

    url = "https://research.investors.com/services/ChartService.svc/GetData" 
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    json = { "req": { "Symbol": code, "Type": 1, "StartDate": "2021-10-13T16:10:50.202Z", "EndDate": "2021-10-13T16:10:50.202Z", "EnableBats": True } }

    r = requests.post(url, headers=headers, json=json)
    r.encoding = "UTF-8"
    result = r.json()
    #print(result)
    rMap = {}

    if 'GetDataResult' in result:
        if result['GetDataResult']['companyInfo']['industryGroup']:
            rMap['industry'] = result['GetDataResult']['companyInfo']['industryGroup']
            rMap['rsRating'] = result['GetDataResult']['rSRating']
            rMap['epsRating'] = result['GetDataResult']['ePSRating']
            rMap['mktDate'] = result['GetDataResult']['marketDate']
    
    return rMap

def get_rs_message(code):

    rMap = rs_rating(code)
    passage = None
    if rMap:
        passage = u'\U0001F6B4' + "<i>RS for %s</i>" % (code.upper()) + EL
        passage = passage + "Industry: %s" % rMap['industry'] + EL
        passage = passage + "rsRating: %s" % rMap['rsRating'] + EL
        passage = passage + "epsRating: %s" % rMap['epsRating'] + EL   
        passage = passage + "Market Date: %s" % rMap['mktDate']
        
    return passage
   
def main(args):

    for code in ("AAPL", "BABA", "JPM", "HELLO"):
        print(get_rs_message(code))

if __name__ == "__main__":
    main(sys.argv)                
              



