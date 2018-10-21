#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from market_watch.util import selenium_helper
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_posts_list(group, utype='p'):

    url = "https://m.weibo.cn/%s/%s" % (utype, group)

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    html = selenium_helper.get_content(url, 1) 

    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    
    #<span class="txt-shadow">sky财经工作室</span>
    #<div class="weibo-text">

    btitle = soup.find('span', {'class': 'txt-shadow'}).text
    urls = soup.find_all("a", href=re.compile("^/status/"))
    titles = soup.find_all("div", {'class': 'weibo-text'})

    print(btitle)
    post_list = []
    title_list = []
    
    for url in urls:
        post_list.append(url['href'].split('/')[-1])
   
    for title in titles:
        title = title.get_text()
        title_list.append(title)
 
    print("Post List Size: %s" % len(post_list))
    return btitle, post_list, title_list

def push_posts_list(group, btitle, plist, tlist, tg_group):

    rkey = "WB:" + group
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

    #get_count = 1
    for idx, pid in enumerate(plist[:get_count]):

        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            new_posts_list.append(pid)
            url = "https://m.weibo.cn/status/%s" % (pid)
            message = tlist[idx] + DEL
            message = message + url
            messages_list.append(message)
    
    #print("BEFORE Post List %s" % posts_list)
    posts_list = new_posts_list + posts_list
    #print("AFTER Posts List %s" % posts_list)
    #print("AFTER Posts List (Limited) %s" % posts_list[:NEW_POSTS_COUNT])
    new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
    redis_pool.setV(rkey, new_json_arr)         
    send_count = 1
    
    for msg in messages_list:
    
        if (send_count == 1):
            msg  = u'\U0001F4F0' + (" <b>Latest Weibo for</b> %s" % btitle) + DEL + msg
        
        print("Msg sent: [%s]" % msg)
        bot_sender.broadcast_list(msg, tg_group)
        
        send_count = send_count + 1

def distribute_posts(grpList, tg_group, isTest=False):

    if (isTest):
        grpList = [
                    ('1005056735409154', 'p'),
                    ('1649159940', 'u'),
                    #('unclesiu', True),
                    ]
        tg_group = "telegram-chat-test"

    for group in grpList:
        [title, plist, tlist] = get_posts_list(group[0], group[1])
        print(title)
        print(plist)
        print(tlist)
        push_posts_list(group=group[0], btitle=title, plist=plist, tlist=tlist, tg_group=tg_group)

    
def main():

    isTest = False

    grpList = [
                ('1005056735409154', 'p'), #Sky Sir
                ('1649159940', 'u')
                ]
    tg_group = "telegram-notice"
    distribute_posts(grpList, tg_group, isTest)


if __name__ == "__main__":
    main()        
        

