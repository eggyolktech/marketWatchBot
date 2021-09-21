#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse as urlparse
import requests
import re
from datetime import datetime
import json
import sys

from market_watch.telegram import bot_sender
from market_watch.util import selenium_helper
from market_watch.redis import redis_pool

DEL = "\n\n"
EL = "\n"

NEW_POSTS_COUNT = 30
GET_POSTS_COUNT = 10
 
def news(cat, subcat):

   
    url = "http://emwap.eastmoney.com/info/list/%s/%s" % (cat, subcat)
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    r.encoding = "UTF-8"
    html = r.content
    soup = BeautifulSoup(html, "html.parser")

    #print(soup.prettify())  
    passages = [] 
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    div = soup.find("div", {"class": "info-list"})
    lis = div.find("ul", {"class": "list"}).find_all("li")

    for li in lis:
        url = li.find("a")['href']
        code = li.find("a")['data-infocode']
        ltitle = li.find("div").text.strip()
        ltimetext = li.find("p").text.strip()

        print("%s (%s)" % (ltitle, ltimetext))

        passage = u'\U0001F3E0' + "<a href='http://emwap.eastmoney.com%s'>%s</a> (%s)" % (url,ltitle, ltimetext)
        #print(passage)
        passageid = code 
        passages.append((passageid, passage))

    return passages

def send_news(cat, subcat):

    passages = news(cat, subcat)
    print(passages)
    
    rkey = "NEWS:EASTMONEY" + cat + subcat
    json_arr = redis_pool.getV(rkey)
    posts_list = []
    messages_list = []
    new_posts_list = []

    if (json_arr):
        print("Posts Redis Cache exists for [%s]" % rkey)
        json_arr = json_arr.decode()
        posts_list = json.loads(json_arr)
        print("Loaded Posts List %s" % posts_list)
        get_count = GET_POSTS_COUNT
    else:
        get_count = NEW_POSTS_COUNT

    for passage in passages[:get_count]:

        pid = passage[0]
        ptext = passage[1]

        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            print(ptext)
            new_posts_list.append(pid)
            bot_sender.broadcast_list(ptext, "telegram-zerohedge")
            #bot_sender.broadcast_list(ptext)
  
            #print("BEFORE Post List %s" % posts_list)
            posts_list = new_posts_list + posts_list
            #print("AFTER Posts List %s" % posts_list)
            #print("AFTER Posts List (Limited) %s" % posts_list[:NEW_POSTS_COUNT])
            new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
            redis_pool.setV(rkey, new_json_arr)
    
def main(args):

    send_news('8', '351')
    send_news('105', '436')

if __name__ == "__main__":
    main(sys.argv)                
              



