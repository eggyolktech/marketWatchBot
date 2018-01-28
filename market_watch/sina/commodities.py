#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

def get_commodities():

    DEL = "\n\n"
    EL = "\n"

    url = "http://stock.finance.sina.com.cn/futures/view/Goods_index.php"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = "gb2312"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    cTables = soup.findAll("table", {"class": "bj_table"})
    passage = "<b>商品價格 (Sina Finance)</b>" + DEL

    for table in cTables:

        for tr in table.findAll("tr")[1:]:

            cols = tr.findAll("td")
            a = cols[0].find('a', href=True)
            href = a['href']
            name = "<a href='" + href + "' target='_blank'>" + cols[0].text + "</a>"
            last = cols[1].text
            change = cols[2].text

           
            if ("-" in change):
                change = change.replace("-", u'\U0001F53B')
            else:
                change = u'\U0001F332' + change

            passage = passage + name + ": " + last + " " + change + EL
   
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
              



