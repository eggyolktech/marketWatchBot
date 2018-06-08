#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_posts_list(group):

    url = "https://zhuanlan.zhihu.com/%s" % group

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 

    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("li", {"class": "ArticleItem"})
    posts_list = []
    
    for article in articles:
        art_a = article.find("a", {"class": "ArticleItem-Excerpt"})
        
        if (art_a):
            url = art_a['href']
            title = article.find("h3", {"class": "ArticleItem-Title"}).text.strip()
            post = {"url": url, "title": title}        
            posts_list.append(post)
    
    print("Post List Size: %s" % len(posts_list))
    return posts_list

def push_posts_list(group, plist, tg_group):

    rkey = "ZH:" + group
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
        
        pid = post['url'].split("/")[-1]
    
        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            new_posts_list.append(pid)
            message = "%s\n%s" % (post['title'], post['url'])
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
            msg  = u'\U0001F4F0' + " <b>Latest Zhihu Updates</b>" + DEL + msg
        
        print("Msg sent: [%s]" % msg)
        bot_sender.broadcast_list(msg, tg_group)
        
        send_count = send_count + 1
    
def main():

    isTest = True 
        
    grpList = ['diqiuzhishiju', #地球知识局
              ]
    
    if (isTest):
        grpList = []
        tg_group = "telegram-chat-test"
    else:
        tg_group = "telegram-notice"

    for group in grpList:
        plist = get_posts_list(group)
        push_posts_list(group, plist, tg_group) 

if __name__ == "__main__":
    main()        
        

