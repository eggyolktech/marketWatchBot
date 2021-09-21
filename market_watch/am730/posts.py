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
import sys, traceback

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_posts_list(group):

    url = "https://www.am730.com.hk/columnist/%s" % group

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    #r.encoding = r.apparent_encoding
    #html = r.text 
    html = selenium_helper.get_content(url, 1)
    #print(html) 
    #soup = BeautifulSoup(html, "html.parser")
    soup = BeautifulSoup(html, "html5lib")
    #print(soup)
    #print(soup.find("main").find("div", {'id': 'columns-page-content-list'}))

    author = soup.find("div", {"class": "columnist_name"}).text.strip()  
    posts_list = []
    options = soup.find("select", {"class": "all_articles_selector"}).find_all("option")
    print(len(options))
    
    for option in options[1:]:
        print(option)
        link = option['value']
        ltitle  = "[%s] %s" % (author, option.text.strip())  
        post = (link, ltitle)
        posts_list.append(post)
        print(post)    
   
    print("Post List Size: %s" % len(posts_list))
    return posts_list

def push_posts_list(group, plist, tg_group, excerpt=False):
    
    rkey = "AM730:" + hashlib.sha1(group.encode('utf-8')).hexdigest()
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
            msg  = u'\U0001F4F0' + " <b>Latest Posts Updates</b>" + DEL + msg
        
        print("Msg sent: [%s]" % msg)
        bot_sender.broadcast_list(msg, tg_group)
        
        send_count = send_count + 1

def distribute_posts(grpList, tg_group, isTest=False):

    if (isTest):
        tg_group = "telegram-chat-test"

    for group in grpList:

        try:
            plist = get_posts_list(group[0])
            push_posts_list(group=group[0], plist=plist, tg_group=tg_group, excerpt=group[1])
        except:
            print("Failing sending to group [%s]" % group[0])
            traceback.print_exc(file=sys.stdout)    

def main():

    isTest = False 

    grpList = [
               #('%E8%AA%AA%E6%A8%93%E8%A7%A3%E6%8C%89%3A%20%E7%8E%8B%E7%BE%8E%E9%B3%B3', True), #王美鳳
               #('%E8%B1%AA%E5%AE%85%E7%9C%9F%E6%9D%8E%3A%20%E6%9D%8E%E5%B7%8D', True), #李巍 
               #('%E6%B9%AF%E6%96%87%E4%BA%AE%E5%B0%88%E6%AC%84%3A%20%E6%B9%AF%E6%96%87%E4%BA%AE', True), #湯文亮 
               ('%E6%94%BF%E7%B6%93%E5%AF%86%E7%A2%BC%3A%20%E5%91%A8%E9%A1%AF', True), #Chow Hin
               ('C%E8%A7%80%E9%BB%9E%3A%20%E6%96%BD%E6%B0%B8%E9%9D%92', True), #C WING CHING
               #('%E9%88%BA%E6%88%90%E5%85%B6%E4%BA%8B%3A%20%E6%9B%BE%E9%88%BA%E6%88%90', True), #TSANG YUK SING
               ]
    tg_group = "telegram-notice"
    distribute_posts(grpList, tg_group, isTest)

if __name__ == "__main__":
    main()        
        

