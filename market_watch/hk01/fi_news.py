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
import feedparser
from time import gmtime
import time
import hashlib

from market_watch.telegram import bot_sender
from market_watch.util import selenium_helper
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

DEL = "\n\n"
EL = "\n"

NEW_POSTS_COUNT = 30
GET_POSTS_COUNT = 10
 
def push_rss_news_alerts_with_redis(url):

    print("Url: [" + url + "]")
    full_message = ""
    messages_list = []
    new_posts_list = []

    posts = feedparser.parse(url)
    url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
    ftitle = posts['feed']['title']

    rkey = "NEWS:HK01" + str(url_hash)
    json_arr = redis_pool.getV(rkey)
    posts_list = []

    if (json_arr):
        print("Posts Redis Cache exists for [%s]" % url)    
        json_arr = json_arr.decode()
        posts_list = json.loads(json_arr)
        print("Loaded Posts List %s" % posts_list)
        get_count = GET_POSTS_COUNT 
    else:
        get_count = NEW_POSTS_COUNT

    for post in posts.entries[:get_count]:

        if 'published_parsed' in post.keys(): 
            stime = str(time.mktime(post.published_parsed))
        else:
            stime = str(time.mktime(post.updated_parsed))

        stitle = post.title
        stime = str(int(hashlib.md5(stitle.encode()).hexdigest(), 16))
        if "ERROR WHILE FETCHING" in stitle:
            print(stitle)
            return

        if (str(stime) in posts_list):
            print("Post created at %s is OLD! Skip sending...." % (stime))
        else:
            print("Post created at %s is NEW! Prepare for sending...." % (stime))
            new_posts_list.append(stime)
            message = u'\U0001F30F' + " <a href='%s'>%s</a>" % (post.link, stitle)
            messages_list.append(message)

    posts_list = new_posts_list + posts_list
    print("Full Posts List %s" % posts_list[:NEW_POSTS_COUNT])
    new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
    redis_pool.setV(rkey, new_json_arr)    
    return messages_list

def publish_news(url):

    passages = push_rss_news_alerts_with_redis(url) 
    print(passages)

    for passage in passages:
        print(passage)
        bot_sender.broadcast(passage, is_test=False, url_preview=False)
 
def main(args):

    urls = ['https://www.google.com.hk/alerts/feeds/17097742724167324955/5967226054184342794',
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/4157788151833439732']

    for url in urls:
        publish_news(url)

if __name__ == "__main__":
    main(sys.argv)                
              



