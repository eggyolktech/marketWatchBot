#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import re
import time
import requests
import hashlib
from bs4 import BeautifulSoup
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool
from market_watch.util import selenium_helper

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_posts_list():

    url = "https://homebloggerhk.com/category/%E5%8D%9A%E5%AE%A2/"

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    #r.encoding = r.apparent_encoding
    html = r.text 
    #print(html) 
    soup = BeautifulSoup(html, "html.parser")
    #soup = BeautifulSoup(html, "html5lib")
    #print(soup.find("main").find("div", {'id': 'columns-page-content-list'}))
    hhs = soup.find_all("h2", {"class": "blog-title"})
    posts_list = []

    for hh in hhs:
        link = hh.find("a")
        ltitle = link.text.strip()
        post = (link['href'], ltitle)
        posts_list.append(post)
    
    print("Post List Size: %s" % len(posts_list))
    print(posts_list)
    return posts_list

def push_posts_list(plist, tg_group, excerpt=False):
    
    rkey = "HOMEBLOGGER:BLOGS"
    print(rkey)
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

    for post in plist[:get_count]:

        purl = post[0]
        ptitle = "%s" % (post[1])
        pid = purl.split("=")[-1]
        #print("pid %s" % pid)    

        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            new_posts_list.append(pid)
            
            message = ptitle + DEL
            message = message + purl
            #print(message)
            messages_list.append(message)
    
    print("BEFORE Post List %s" % posts_list)
    posts_list = new_posts_list + posts_list
    print("AFTER Posts List %s" % posts_list)
    print("AFTER Posts List (Limited) %s" % posts_list[:NEW_POSTS_COUNT])
    new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
    redis_pool.setV(rkey, new_json_arr)         
    send_count = 1
    
    for msg in messages_list:
    
        if (send_count == 1):
            msg  = u'\U0001F4F0' + " <b>HomeBlogger Posts Updates</b>" + DEL + msg
        
        print("Msg sent: [%s]" % msg)
        bot_sender.broadcast_list(msg, tg_group)
        
        send_count = send_count + 1

def distribute_posts(tg_group, isTest=False):

    if (isTest):
        tg_group = "telegram-chat-test"

    plist = get_posts_list()
    push_posts_list(plist=plist, tg_group=tg_group)
    
def main():

    isTest = False 

    tg_group = "telegram-homeblogger"
    distribute_posts(tg_group, isTest)

if __name__ == "__main__":
    main()        
        

