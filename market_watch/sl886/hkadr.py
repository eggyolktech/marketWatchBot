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

def add_sign_flag(change, is_pos):

    if (not is_pos):
        change = u'\U0001F53B' + change.replace("(","").replace(")","")
    else:
        change = u'\U0001F332' + change.replace("(","").replace(")","")

    return change


def add_sign(change):

    if (change == "0"):
        change = change
    elif ("-" in change):
        change = change.replace("-", u'\U0001F53B')
    else:
        change = u'\U0001F332' + change

    return change

def get_hkadr():

    DEL = "\n\n"
    EL = "\n"

    url = "https://docs.google.com/spreadsheets/d/18gKRb-tOcg9lmklqBiOY73KVuf0zHNz3IZJNeWwGjJA/pubhtml/sheet?headers=false&gid=0"

    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = None

    try:
        r = requests.get(url, headers=headers, timeout=10)
    except:
        print("Timeout once.... Try again...")
        r = requests.get(url, headers=headers, timeout=10)
    #r.encoding = "gb2312"
    html = r.text
 
    soup = BeautifulSoup(html, "html.parser")
    passage = ""
    #print(html)
    tbody = soup.find("table", {"class":"waffle"}).find("tbody")
    
    if (tbody):
        passage = "<b>即時ADR港股比例指數 (adr168.com)</b>" + DEL
    
    isAdrStart = False

    for tr in tbody.findAll("tr"):

        if "ADR國比指數" in tr.text:
            print("End Looping...")
            break
 
        elif "恆生指數" in tr.text: 
        
            cols = tr.findAll("td")
            symbol = cols[2].text

            if "-" in cols[4].text:
                is_pos = False
            else:
                is_pos = True

            idxclose = add_sign_flag(cols[3].text, is_pos)
            changepx = add_sign(cols[4].text)
            passage = passage + "%s: %s %s" % (symbol, idxclose, changepx) + DEL          

        elif "ADR港" in tr.text:

            cols = tr.findAll("td")
            symbol = cols[0].text

            if "-" in cols[2].text:
                is_pos = False
            else:
                is_pos = True

            idxclose = add_sign_flag(cols[1].text, is_pos)
            changepx = add_sign(cols[2].text)
            passage = passage + "%s: %s %s" % (symbol, idxclose, changepx) + DEL

        elif "成份股" in tr.text:
            isAdrStart = True

        elif isAdrStart:

            cols = tr.findAll("td")
            symbol = cols[0].text
            
            if (symbol.strip() and not "指數" in symbol.strip()):
                if "-" in cols[3].text:
                    is_pos = False
                else:
                    is_pos = True

                stkclose = add_sign_flag(cols[2].text, is_pos)
                stkclose_adr = add_sign_flag(cols[6].text, is_pos)
                volume = cols[5].text
                changepx = add_sign(cols[3].text)
                changepercent = add_sign_flag(cols[4].text, is_pos)
                #passage = passage + "%s: %s %s (%s)" % (symbol, stkclose, changepx, changepercent) + DEL
                passage = passage + "%s: %s %s (%s%%)" % (symbol, stkclose, changepx, changepercent) + DEL
     
            #txttmpl = "%s: %s %s (%s)"
            #passage = passage + txttmpl % (symbol, add_sign_flag(adrs, is_pos), add_sign(changept), add_sign(change_px)) + DEL

    if (not passage):
        passage = "No adr info found."
    
    return passage   

def get_hkadr_sl886():

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
              



