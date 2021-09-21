#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse as urlparse
import requests
import re
from datetime import datetime

from market_watch.telegram import bot_sender
from market_watch.db import profit_warning_db
from market_watch.etnet import result_announcement
from hickory.crawler.aastocks import stock_info

DEL = "\n\n"
EL = "\n"
 
def get_latest_reports(period, reporttype=1):

   
    if (reporttype == 1): 
        url = "http://www.etnet.com.hk/www/tc/news/special_news_list.php?category=%E4%BC%81%E6%A5%AD%E7%9B%88%E5%96%9C"
    elif (reporttype == 2):
        url = "http://www.etnet.com.hk/www/tc/news/special_news_list.php?category=%E4%BC%81%E6%A5%AD%E7%9B%88%E8%AD%A6"
    else:
        print("Invalid Report Type")
        return

    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
   
    passages = [] 
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    divTag = soup.find_all("div", {"class": "DivArticleList"})

    for tag in divTag:
        dateTags = tag.find_all(['p', 'span'], {"class": "date"})
        a = tag.find('a')
        #newsTags = tag.find_all("p", {"class": "ArticleHdr"})
       
        for idx, tag in enumerate(dateTags):
            
            aURL = a['href']
            aURL = "http://www.etnet.com.hk/www/tc/news/" + aURL
            parsed = urlparse.urlparse(aURL)
            key = urlparse.parse_qs(parsed.query)['newsid']
            #print(str(tag.text.strip()) + " - " + str(key))
            if (not profit_warning_db.add_warning(tag.text.strip(), key[0], str(reporttype))):
                print("Logtime already reported before: [" + tag.text.strip() + " - " + key[0] + "]")
                break
          
            industry = None 
            if (len(a.text.split("（")) > 1):
                code = a.text.split("（")[1].split("）")[0]
                code = code.replace("１","1").replace("２","2").replace("３","3").replace("４","4").replace("５","5").replace("６","6").replace("７","7").replace("８","8").replace("９","9").replace("０","0")
                if (stock_info.get_info(code)):
                    industry = stock_info.get_info(code)["industry"]
            
            passage = "<a href='" + aURL + "' target='_blank'>" + a.text + "</a> (" + tag.text + ")" + EL
            if (industry):
                passage = passage + "行業版塊: " + industry + " - /qQ" + code
            passages.append(passage)   

    return passages 
    
def main():

    # profit warning (+ve)
    #for report in get_latest_reports(40, 1):
    #    print(report)
    #    bot_sender.broadcast(report)

    # profit warning (-ve)
    #for report in get_latest_reports(40, 2):
    #    print(report)
    #    bot_sender.broadcast(report)

    # result annountcement (aastocks)
    for passage in result_announcement.get_latest_result_announcement():
        print(passage)
        bot_sender.broadcast(passage, False, False)
   
if __name__ == "__main__":
    main()                
              



