#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse as urlparse
import requests
import re
from datetime import datetime
from collections import OrderedDict 
from market_watch.telegram import bot_sender
from market_watch.db import profit_warning_db
from market_watch.etnet import result_announcement
from hickory.crawler.aastocks import stock_info

DEL = "\n\n"
EL = "\n"

def get_top_etf_holdings():

    passage_list = []
    for url in [
                #'https://etfdb.com/compare/highest-52-week-returns/no-leveraged/', 
                'https://etfdb.com/compare/highest-ytd-returns/no-leveraged/',
                'https://etfdb.com/compare/highest-13-week-returns/no-leveraged/', 
                'https://etfdb.com/compare/highest-monthly-returns/no-leveraged/', 
                'https://etfdb.com/compare/highest-weekly-returns/no-leveraged/']:
        passage_list.append(get_top_etf_ind_holdings(url))

    return passage_list


def get_top_etf_ind_holdings(url, limit=25):

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, verify=False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    passage = ""
    ptitle = soup.find("div", {"class": "mm-heading-no-top-margin"}).text.strip()
    ptitle = ptitle.replace("100", str(limit))

    table = soup.find("table", {"class": "mm-mobile-table"})
    rows = table.find("tbody").find_all("tr")
    count = 1  
 
    for row in rows:
        cols = row.find_all("td")
        desc = cols[1].text.strip()
        if "VIX" not in desc:
            passage = passage + ("%s - %s" % (count, desc)) + EL
            passage = passage + ("/qH%s +%s, AUM:%s" % (cols[0].text.strip(), cols[2].text.strip(), cols[3].text.strip())) + EL
            passage = passage + ("/qv%s Avg Vol:%s" % (cols[0].text.strip(), cols[4].text.strip())) + DEL
            count = count + 1
        
        if count > limit:
            break

    if passage:
        passage = u'\U0001F514' + ptitle + DEL + passage

    return passage

def get_etf_profile(code):
   
    url = "https://etfdb.com/etf/%s/#holdings" % code.upper()
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, verify=False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    hname = soup.find("h1", {"class": "data-title"})
    try:
        etf_name = hname.text.strip().replace("\n", " ")
    except:
        return "Profile data for this ETF is not available."
    
    try:
        divprofile = soup.find("div", {"id": "overview"})
        uls = divprofile.find_all("ul", {"class": "list-unstyled"})
        desc = soup.find("div", {"id": "analyst-report"}).find("p").text.strip()
        print(desc)
    except:
        return "Profile data for this ETF is not available."

    ep = OrderedDict()
    ep['Description'] = desc
    for ul in uls:
        lis = ul.find_all("li")
        for li in lis:
            ekey = li.find_all("span")[0].text.strip()
            eval = li.find("span", {"class", "pull-right"}).text.strip()
            
            if ekey == 'ETF Home Page':
                try:
                    eval = "<a href='%s'>Home Page</a>" % li.find("span", {"class", "pull-right"}).find("a")['href']
                except:
                    eval = li.find("span", {"class", "pull-right"}).text.strip()
            ep[ekey] = eval

    print(ep)

    for key, value in ep.items(): 
        passage = passage + "%s: %s" % (key, value) + EL
    
    if passage:
        passage = u'\U0001F514' + " Profile Data for %s" % etf_name + DEL + passage

    return passage
 

def get_etf_holdings(code):
   
    url = "https://etfdb.com/etf/%s/#holdings" % code.upper()
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, verify=False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    hname = soup.find("h1", {"class": "data-title"})
    try:
        etf_name = hname.text.strip().replace("\n", " ")
    except:
        return "Holdings data for this ETF is not available."
    print('etf_name %s' % etf_name)    
    try:
        table = soup.find("table", {"data-hash": "etf-holdings"})
        rows = table.find("tbody").find_all("tr")
    except:
        return "Holdings data for this ETF is not available."

    count = 1
    for row in rows:
        cols = row.find_all("td")
        ecode = cols[0].text.strip()
        if len(ecode) < 5 and ecode.isalpha():
            passage = passage + "%s - /qv%s %s (%s)" % (count, ecode, cols[1].text, cols[2].text) + EL
        else:
            passage = passage + "%s - %s - %s (%s)" % (count, ecode, cols[1].text, cols[2].text) + EL
        count = count + 1

    if passage:
        passage = u'\U0001F514' + " Top 15 Holdings for %s" % etf_name + DEL + passage

    return passage
    
def main():

    for code in ['IBUY','IHAK']:
        passage = get_etf_holdings(code)
        #passage = get_etf_profile(code)
        print(passage)
    #plist =  (get_top_etf_holdings())
    #for p in plist:
    #    bot_sender.broadcast(p, True)
   
if __name__ == "__main__":
    main()                
              



