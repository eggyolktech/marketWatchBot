#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import re
from datetime import date
from datetime import datetime
from market_watch.telegram import bot_sender
from market_watch.util import config_loader

# load config
config = config_loader.load()

def get_etf_stat(url):

    passage = ""

    print("ETF Url: [" + url + "]")
    
    r = requests.get(url, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    table = soup.find('table', id="tblTS2")
    tbody = table.find('tbody')
    rows = tbody.findAll('tr')
    
    count = 0
    
    # skip the skewed records
    for row in rows[1:]:
    
        if (count == 10):
            break
            
        count = count + 1
                
        _etfname = row.select('td')[0].text
        _etfcode = row.select('td')[1].text
        
        _dps = row.select('td')[2].text
        _latesty = row.select('td')[3].text
        _last1yry = row.select('td')[4].text
        _last2yry = row.select('td')[5].text
        _last3yry = row.select('td')[6].text
        _3yravgy = row.select('td')[7].text
        _policy = str(row.select('td')[8].text)
        _policy = re.sub(r'[^\x00-\x7F]+','', _policy)
        
        passage = passage + "<b>" + str(count) + ". " + _etfname + " (" + _etfcode + ")" + "</b>" + "\n" + "DPS " + _dps + " <i>@" + _latesty + "</i> " + _policy + "\n\n"

    if (passage == ""):
        passage = "No ETFs record for today."
    else:
        passage = "<b>Top 10 ETFs with highest dividends</b>\n\n" + passage
    
    print("Passage: [" + passage + "]")
    return passage

def get_hy_stat(url, industry):

    passage = ""
    
    print("Url: [" + url + "]")
    
    r = requests.get(url, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    table = soup.find('table', id="tblTS2")
    tbody = table.find('tbody')
    rows = tbody.findAll('tr')
    
    count = 0
    
    # skip the skewed records
    for row in rows:
    
        if (count == 10):
            break
            
        count = count + 1
        
        _name = row.select('td')[0].select('div')[0].select('div')[0].select('span')[0].text
        _code = row.select('td')[0].select('a')[0].text
        
        _quote = row.select('td')[2].text
        _peratio = row.select('td')[7].text
        _pbratio = row.select('td')[8].text
        _yield = row.select('td')[9].text
        _marketcap = row.select('td')[10].text  

        print(_name)
        print(_code)
        
        passage = passage + "<b>" + str(count) + ". " + _name + " (" + _code + ")" + "</b>" + "\n" + "$" + _quote + " <i>@" + _yield + ", P/E(x): " + _peratio + ", P/B(x): " + _pbratio +"</i> MCP: " + _marketcap + "\n\n"

    if (passage == ""):
        passage = "No bank stock records for today."
    else:
        passage = "<b>Top 10 " + industry + " with highest dividends</b>\n\n" + passage
    
    print("Passage: [" + passage + "]")
    return passage
    
def main():

    passage = get_etf_stat(config.get("aastocks","hy-url-etf"))

    bot_sender.broadcast(passage)

    url_list = config.items("aastocks-hy-industry")

    for key, url in url_list:
        print("Industry to retrieve: " + key + " => " + url)

        passage = get_hy_stat(url, key.split("-")[-1])
        bot_sender.broadcast(passage)

if __name__ == "__main__":
    main()                
              



