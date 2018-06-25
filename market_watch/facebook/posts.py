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

    url = "https://www.facebook.com/pg/%s/posts/?ref=page_internal" % group

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 

    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div", id=re.compile("^feed_subtitle_"))
    
    posts_list = []
    
    for div in divs:
        idlist = div.get('id').split(";")

        if (len(idlist) > 1):
            posts_list.append(idlist[1].strip())
    
    print("Post List Size: %s" % len(posts_list))
    return posts_list

def push_posts_list(group, plist, tg_group):

    rkey = "FB:" + group
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

    for pid in plist[:get_count]:
    
        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            new_posts_list.append(pid)
            message = "https://www.facebook.com/%s/posts/%s" % (group, pid)
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
    
def main():

    isTest = False 
        
    grpList = ['ivanliresearch', #Ivan Li 李聲揚 - 華麗后台
                'DrLamInv', #Dr Lam
                'sky788', #張士佳 - Sky Sir
                '112243028856273', #英之見 - 基金經理黃國英Alex Wong
                'eddietamcai', #Eddie Team
                'thinkingweb',
                'Starmancapital', #Starman 資本攻略
                ]
    
    if (isTest):
        grpList = []
        tg_group = "telegram-chat-test"
    else:
        tg_group = "telegram-notice"

    for group in grpList:
        plist = get_posts_list(group)
        push_posts_list(group, plist, tg_group)          

    grpList = [
                'SimonIRBasilica', #平行時空：沈旭暉國際學術新聞台
                'shensimon', #堅離地城：沈旭暉國際生活台 Simon's Glocal World
                'SimonStamps', #萬國郵政 Simon's Stamps International
                'mshktech', #Microsoft HK Technical Community
                'parentingtw',
                'hk01parenting',
                #'parenting.reading',
                #'parenting.lifebuzz', #親子天下‧寶寶生活
                'gushi.tw',
                ]

    if (isTest):
        grpList = ['gushi.tw',]
        tg_group = "telegram-chat-test"
    else:
        tg_group = "telegram-itdog"
        
    for group in grpList:
        plist = get_posts_list(group)
        push_posts_list(group, plist, tg_group)

if __name__ == "__main__":
    main()        
        

