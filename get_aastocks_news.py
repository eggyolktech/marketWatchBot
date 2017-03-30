from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

def get_latest_news_by_code(code, number):

    DEL = "\n\n"
    EL = "\n"
    URL = "http://www.aastocks.com"

    if (is_number(code) and is_number(number)):
        print("Code to Quote: [" + code + "]")
        print("Number to Grab: [" + str(number) + "]")           
    else:
        return "<i>Usage:</i> " + "/qn" + "[StockCode] (e.g. " + "/qn2899" + ")"   
    
    url = "http://www.aastocks.com/tc/stocks/news/aafn-company-news/%s/0/all/1/1" % (code)
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    
    passage = ""
    
    #<div class="content_box"> <div id="cp_ucAAFNSearch_repIndNews_pIISNews_0"> <div class="newshead2 mcFont2  font16imp lettersp2 "> <img class="vam" src="/tc/resources/images/common/icon_iis.png">&nbsp;<a class="h6" href="http://iis.aastocks.com/20170329/002761544-0.PDF" title="《HKEx》- 00939 建設銀行 - 董事會審計委員會2016年度履職情況報告" target="_blank">
#《HKEx》- 00939 建設銀行 - 董事會審計委員會2016年度履職情況報告
#</a> </div> <div class="newstime2">發放時間&nbsp;2017/03/29 21:22</div> <div class="newstime2">公告及通告</div> </div> </div>

    for div in soup.findAll('div', id=re.compile("^cp_ucAAFNSearch_repIndNews_pIISNews"))[:number]:
    
            a = div.find('a', {"class", "h6"})
            t = div.find('div', {"class", "newstime2"})
            
            passage = passage + DEL + "<a href='" + a['href'] + "' target='_blank'>" + a['title'] + "</a> (" + t.getText()[-11:] + ")" 
    
    if (not passage):
        passage = "No news is good news!"
    else:
        passage = "<i>Latest News Feed for " + code + ".HK</i>" + passage
    
    return passage   
    
def main():

    print(get_latest_news_by_code("939", 5).encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



