#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
from market_watch.fxcm import live_rate


def get_futures(contract, params):

    DEL = "\n\n"
    EL = "\n"

    if ("hscei" in params):
        if (contract == "N"):
            fut = "20020"
        else:
            fut = "20030"
    else:
        if (contract == "N"):
            fut = "20000"
        else:
            fut = "20010"

    if ("next" in params):
        ure = "1"
    else:
        ure = "0"

    url = "http://www.aastocks.com/tc/stocks/market/bmpfutures.aspx?future=%s%s" % (fut, ure)
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=10)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("div", {"class": "grid_11"}).findAll("option", selected=True)[0].text

    fuDiv = soup.find("div", {"class": "content"})
    fuTable = fuDiv.find("table", {"class": "tblM"})

    passage = "<b>" + title +  "</b>" + DEL

    rows = fuTable.findAll("tr", recursive=False)
    col = rows[0].findAll("td")[0]
    
    last = col.find("div", {"class": "font26"}).text.strip()
    last_update_time = col.find("div", {"class": "rmk2"}).find("span").text
    range_today = col.findAll("span", {"class": "float_r"})[1].text

    col = rows[0].findAll("td")[1]
    change = col.find("div", {"class": "font18"}).text.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')

    col = rows[0].findAll("td")[2]
    premium = col.find("div", {"class": "font18"}).text

    col = rows[1].findAll("td")[0]
    change_pct = col.findAll("div", {"class": "font18"})[0].text.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
    
    col = rows[1].findAll("td")[1]
    volume = col.find("div", {"class": "font18"}).text

    range_monthly = rows[2].findAll("td")[0].find("div", {"class": "float_r"}).text
    open_price = rows[2].findAll("td")[1].find("div", {"class": "float_r"}).text
    goi = rows[3].findAll("td")[0].find("div", {"class": "float_r"}).text
    goi_change = rows[3].findAll("td")[1].find("div", {"class": "float_r"}).text.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
    noi = rows[4].findAll("td")[0].find("div", {"class": "float_r"}).text
    noi_change = rows[4].findAll("td")[1].find("div", {"class": "float_r"}).text.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
    expiry_date = rows[5].findAll("td")[0].find("div", {"class": "float_r"}).text
    final_date = rows[5].findAll("td")[1].find("div", {"class": "float_r"}).text
    underlying = rows[6].findAll("td")[0].text.replace("相關資產", "").replace("恆生指數", "").strip().replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
 
    passage = passage + "現價: " + last + EL
    passage = passage + "波幅: " + range_today + EL
    passage = passage + "升跌: " + change + " (" + change_pct + ")" + EL
    passage = passage + "溢價: " + premium + EL
    passage = passage + "成交量: " + volume + EL
    passage = passage + "月波幅: " + range_monthly + EL
    passage = passage + "開市: " + open_price + EL
    passage = passage + "未平倉合約總數: " + goi + " (" + goi_change + ")" + EL
    passage = passage + "未平倉合約淨數: " + noi + " (" + noi_change + ")" + EL
    passage = passage + "到期日: " + expiry_date + EL
    passage = passage + "最後結算日: " + final_date + EL
    passage = passage + "相關指數: " + underlying + EL
    passage = passage + "最後更新: " + last_update_time + EL 

#        change = change.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')
 #       change_pct = change_pct.replace("+", u'\U0001F332').replace("-", u'\U0001F53B')

    
    if (not passage):
        passage = "No futures found."
    
    return passage   
    
def main():

    print(get_futures("M", [""]))
    print(get_futures("N", ["next"]))
    print(get_futures("M", ["hscei"]))
    print(get_futures("N", ["next", "hscei"]))
    print(get_futures("M", ["hscei", "next"]))

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



