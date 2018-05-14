#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from market_watch.redis import redis_pool

DEL = "\n\n"
KEY = "OPTIONS:List"

def set_options_code_list():

    url = "https://www.chiefgroup.com.hk/en/options/contract-table#collapseOne"

    #print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
   
    codes = soup.findAll("td", {"data-label": "SEHK Code"})

    code_list = []

    for code in codes:
        code_list.append(code.text.strip().zfill(5))

    print("Set List: %s" % code_list)
    redis_pool.setV(KEY, json.dumps(code_list))

def get_options_code_list():

    json_arr = redis_pool.getV(KEY)
    code_list = []
    #print(json_arr)
    if (json_arr):
        json_arr = json_arr.decode()        
        code_list = json.loads(str(json_arr))
        print("Loaded List: %s" % code_list)

def is_option_code(code):

    json_arr = redis_pool.getV(KEY)
    code_list = []
    code = code.zfill(5)
    
    if (json_arr):
        json_arr = json_arr.decode()
        if (code in json_arr):
            return True
        else:
            return False

def main():

    set_options_code_list()
    get_options_code_list()

    for code in ["1","2","175","1357","87001"]:
        print(is_option_code(code))

if __name__ == "__main__":
    main()        
        

