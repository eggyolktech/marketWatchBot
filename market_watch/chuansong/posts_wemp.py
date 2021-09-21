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
from market_watch.util import selenium_helper
from market_watch.util import proxy_helper

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_posts_list(group, pjson):

    url = "https://wemp.app/accounts/%s" % group

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    proxies = {}
    
    if pjson:
        
        addr = 'http://%s:%s' % (pjson['ip'], pjson['port'])
        proxies = {
            "http": addr, 
            "https": addr
        }

    try:
        r = requests.get(url, headers=headers, proxies=proxies)
    except:
        
        pjson = proxy_helper.get_proxy()   
        addr = 'http://%s:%s' % (pjson['ip'], pjson['port'])
        proxies = {
            "http": addr, 
            "https": addr
        }
   
        r = requests.get(url, headers=headers, proxies=proxies)

    html = r.text 

    #print(html)
    #return
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", {"class": "post-item__title"})
    
    posts_list = []
    
    for link in links:
        #print(link)
        ptitle = link.text.strip()
        post = ("https://wemp.app%s" % link['href'], link.text.strip(), ptitle)
        posts_list.append(post)
    
    print("Post List Size: %s" % len(posts_list))
    return posts_list

def push_posts_list(group, plist, tg_group, excerpt=False):

    rkey = "WEMP:" + group
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
        ptitle = "[%s] %s" % (post[2], post[1])
        pid = purl.split("/")[-1]
    
        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            new_posts_list.append(pid)
            
            message = ptitle + DEL
            message = message + purl
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

    import random
    pjson = proxy_helper.get_proxy()   

    #group = random.choice(grpList)
    for group in grpList:
        plist = get_posts_list(group[0], pjson)
        push_posts_list(group=group[0], plist=plist, tg_group=tg_group, excerpt=group[1])

    
def main():

    isTest = False 

    pjson = proxy_helper.get_proxy()
    addr = 'http://%s:%s' % (pjson['ip'], pjson['port'])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    proxies = {
        "http": addr,
        "https": addr
    }

    url = 'https://www.facebook.com/pg/Vcp%E5%9E%8B%E6%85%8B-%E8%82%A1%E7%A5%A8%E8%B6%A8%E5%8B%A2%E4%BA%A4%E6%98%93Swing-trade-105888807793932/posts/?ref=page_internal'
    r = requests.get(url, headers=headers, proxies=proxies)

    '''grpList = [
                ('2b591366-8a1b-4848-b952-5c4b12383bff', True), #hunji
                ('0494f495-bb14-486c-9aec-97c28dc4ffb0', True), #kenjinrong
                ('bfbeedd0-4bfb-480a-a5b6-1d6467a2f80d', True), #diqiuzhishiju
                ('6a79c057-ad26-470d-9e6d-e9f8cadff2b1', True), #西西弗评论
                ('d3ca211b-1065-44a7-9924-13b7dbc121bd', True), #hey-stone-money
                ('adb31591-55cb-4027-830c-649890f48ef5', True), #lukewen1982

                ]
    tg_group = "telegram-lpt"
    distribute_posts(grpList, tg_group, isTest)'''
 
if __name__ == "__main__":
    main()        
        

