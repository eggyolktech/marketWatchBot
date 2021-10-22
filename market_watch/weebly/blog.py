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
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

DEL = "\n\n"
EL = "\n"

NEW_POSTS_COUNT = 30
GET_POSTS_COUNT = 10
 
def news():

    url = "https://skycheung.weebly.com/article" 
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    r.encoding = "UTF-8"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")
    div = soup.find("div", {"class": "blog-post"})
    #print("id %s" % div['id'])
    newhash = div['id']
    title = div.find("h2", {"class": "blog-title"}).text
    content = div.find("div", {"class": "paragraph"}).text
    content = "<b>" + title + "</b>" + "\n" + content
    content = content + "\n\n" + url 
    return (newhash, content)  
    
def main(args):

    #return
    rkey = "BLOG:SKYCHEUNG"
    lasthash = redis_pool.getV(rkey)

    if (lasthash):
        print("Last Redis Cache exists for [%s]" % rkey)
        print("Loaded Last Hash: %s" % lasthash)
    else:
        lasthash = b""

    newhash, content = news()

    if (newhash == lasthash.decode()):

        print("Post ID [%s] is OLD! Skip sending...." % (newhash))
    else:
        print("Post ID [%s] is NEW! Prepare for sending...." % (newhash))
        #bot_sender.broadcast(content, is_test=False, url_preview=True)
        bot_sender.broadcast_list(content, "telegram-ptgroup", True)
        redis_pool.setV(rkey, newhash)
    

if __name__ == "__main__":
    main(sys.argv)                
              



