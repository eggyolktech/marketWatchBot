#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

def add_sign_flag(change, is_pos):

    if (not is_pos):
        change = u'\U0001F53B' + change
    else:
        change = u'\U0001F332' + change

    return change


def add_sign(change):

    if (change == "0"):
        change = change
    elif ("-" in change):
        change = change.replace("-", u'\U0001F53B')
    else:
        change = u'\U0001F332' + change

    return change

def get_hkadr_m():

    DEL = "\n\n"
    EL = "\n"

    url = "http://m.hkadr.com/3.php"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=10)
    #r.encoding = "gb2312"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    passage = ""
    print(html)
    lists = soup.findAll("li", {"class":"ui-li-static"})
    
    if (lists):
        passage = "<b>HKADR 環球即市資訊 (m.hkadr.com)</b>" + DEL
    
    for list in lists:
        
        for cells in list.findAll("td"):
            
            symbol = cells[0].text
            adr = cells[2].text
            changept = cells[4].strip().split()[0]
            changepx = cells[4].strip().split()[1]
            
            if "-" in changept:
                is_pos = False
            else:
                is_pos = True
            
            txttmpl = "%s: %s %s (%s)"
            passage = passage + txttmpl % (symbol, add_sign_flag(adrs, is_pos), add_sign(changept), add_sign(change_px)) + DEL

    if (not passage):
        passage = "No adr info found."
    
    return passage   

def get_hkadr():

    DEL = "\n\n"
    EL = "\n"

    url = "http://adr.sl886.com"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=10)
    #r.encoding = "gb2312"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    passage = ""

    divheader = soup.find("div", {"class":"stockheader"})
    
    if (divheader):
        passage = "<b>" + divheader.find(text=True) + "(sl886.com)</b>" + DEL

        adr_txt = divheader.span.text
        adr_style = divheader.span["style"]
        #print(adr_style)
        adrs = adr_txt.split()
        #print(adrs)
        if "red" in adr_style:
            is_pos = False
        else:
            is_pos = True

        passage = passage + add_sign_flag(adrs[0], is_pos) + " " + add_sign_flag(adrs[1], is_pos) + " " + adrs[2] + DEL

    listtable = soup.find("table", {"class":"listtable"})

    for tr in listtable.findAll("tr")[1:-1]:

        cols = tr.findAll("td")
        symbol = cols[0].text.strip()
        adr = "US$" + cols[2].text.strip()
        adrhkd = "HK$" + cols[3].text.strip()
        adrcx = add_sign(cols[4].text.strip())
        adrpx = add_sign(cols[5].text.strip())
        idxcx = add_sign(cols[7].text.strip())

        passage = passage + symbol + ": " + adr + " / " + adrhkd + EL
        passage = passage + adrcx + " (" + adrpx + ") IMPACT: " + idxcx + DEL
   
    if (not passage):
        passage = "No adr info found."
    
    return passage   
    
def main():

    print(get_hkadr())
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



