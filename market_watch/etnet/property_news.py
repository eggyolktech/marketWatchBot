#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse as urlparse
import requests
import re
from datetime import datetime
import json

from market_watch.telegram import bot_sender
from market_watch.util import selenium_helper
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

DEL = "\n\n"
EL = "\n"

NEW_POSTS_COUNT = 30
GET_POSTS_COUNT = 10
 
def news():

   
    url = "http://money18.on.cc/property/news_breaking.html?section=pro"
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    #r = requests.get(url, headers=headers)
    #html = r.text
    html = selenium_helper.get_content(url, 1)
    soup = BeautifulSoup(html, "html.parser")
  
    passages = [] 
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")
    #print(soup)
    divs = soup.find_all("div", {"class": "news_photolist"})

    for div in divs:

        link = div.find("div", {"class": "date"}).find("a")['href']
        time = div.find("div", {"class": "date"}).text
        title = div.find("div", {"class": "title"}).text

        passage = u'\U0001F3E0' + " <a href='http://money18.on.cc%s'>%s</a> (%s)" % (link, title, time)
        passageid = link.split("&")[-1].split("=")[-1]
        passages.append((passageid, passage))

    return passages
    
def main():

    passages = news()

    rkey = "NEWS:MONEY18"
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
            bot_sender.broadcast(ptext, False)
  
            #print("BEFORE Post List %s" % posts_list)
            posts_list = new_posts_list + posts_list
            #print("AFTER Posts List %s" % posts_list)
            #print("AFTER Posts List (Limited) %s" % posts_list[:NEW_POSTS_COUNT])
            new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
            redis_pool.setV(rkey, new_json_arr)
 
if __name__ == "__main__":
    main()                
              



