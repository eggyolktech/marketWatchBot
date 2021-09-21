#!/usr/bin/python


from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from hickory.db import stock_tech_db as stdb, stock_db as sdb
from hickory.crawler.money18 import stock_quote
from datetime import date
from datetime import datetime
from market_watch.telegram import bot_sender
from market_watch.hkex import ccass_loader

def get_gem_ipo_list():


    DEL = "\n\n"
    EL = "\n"
    CL = ":"
    passage = ""
    count = 0
    maxpage = 16

    for i in range(1,maxpage):
        url = "http://www.aastocks.com/tc/ipo/ListedIPO.aspx?iid=ALL&orderby=DA&value=DESC&index=%s" % (i)

        #print("URL: [" + url + "]")  
    
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        r = requests.get(url, headers=headers, timeout=10)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
    
        tableCorp = soup.find('table', {'class', 'newIPOTable'})
    
        if (tableCorp):
    
            trows = tableCorp.findAll("tr", recursive=False)[3:]
        
            for tr in trows:
                code = tr.findAll("td")[1].text.strip()
                if (code.startswith("08")):
                    tobj = stock_quote.get_hk_stock_quote(code)
                    isNotH = not (sdb.get_stock_shstype(code) == "H")
                    print("getting.... " + code + " - " + str(isNotH))
                    if (tobj and isNotH):
                        mktCap = tobj['MktCap']
                        wkLow = float(tobj['52WeekLow'])
                        close = float(tobj['Close'])
                        name = tobj['CodeName']
                        #print(code + "-" + str(wkLow))
                        #print(code + "-" + str(mktCap) + " - " + str(close) + " / " + str(wkLow) + " : " + str(close/wkLow))                        
                        if ("M" in str(mktCap) and wkLow > 0):
                            if float(mktCap.replace("M","")) <= 350 and wkLow > 0  and close/wkLow < 1.4:
                                #print(code + " is HIT")
                                print(code + "-" + str(mktCap) + " - " + str(close) + " / " + str(wkLow))
                                ccass = ccass_loader.get_latest_ccass_info(code.lstrip("0"), 3, True) 
                                if(ccass):
                                    num_p = float(ccass[0])
                                    per = ccass[1]
                                    pname = []
                                    pper = []
                                    totalper = 0
                                    plist = "Top 3 participants: " + EL
                                    isnobank = True

                                    for p in ccass[2:]:
                                        plist = plist + p[1] + " (" + p[3] + ")" + EL
                                        nper = float(p[3].replace("%",""))
                                        if ("銀行" in p[1] and nper > 20):
                                            isnonank = False
                                        totalper = totalper + nper
                                    #print(code + " - " + per)
                                    #print(plist)
                                    
                                    pratio = (totalper / float(per.replace("%","")))
                                    print(code + " - " + str(num_p) + ":" + str(pratio))
                                    if (num_p <= 150 and pratio > 0.6 and isnobank):
                                        passage = passage + "/qQ" + code + " - " + name + EL + "MktCap: " + str(mktCap) + ", CL: " + str(close) + " / 52WL: " + str(wkLow) + EL + "Total # of participants: " + str(num_p) + " (" + per + ")" + EL + plist + EL + "Chart: /qd" + code + DEL

    if (not passage):
        passage = "No Listed IPO!"
    else:
        passage = "<i>Listed GEM IPOs (w. Potential)</i>" + DEL + passage
   
    print(passage) 
    return passage   
    
def main():

    #print(get_gem_ipo_list())
    #bot_sender.broadcast_list(get_gem_ipo_list())
    bot_sender.broadcast_list(get_gem_ipo_list(), "telegram-excel")
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
     
if __name__ == "__main__":
    main()                
              



