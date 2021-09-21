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
from market_watch.util import curl_util
from market_watch.mongodb import watcher_repo as wp
import traceback
import urllib3
import urllib.parse as urlparse
from urllib.parse import parse_qs

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_posts_dict(group):

    #group = 'shensimon'
    #group = 'sspgadgetoutlet'
    
    curl="curl 'https://m.facebook.com/%s/?ref=page_internal' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' -H 'Origin: https://www.example.com' --compressed" % group
    print(curl)
    html = curl_util.call_curl(curl)
    print(html)
    
    soup = BeautifulSoup(html, "html.parser")
    hrefs = soup.find_all("a", href = re.compile(r".*%s\/\?refid=" % group))
    #hrefs = soup.find_all("a", href = re.compile(r'.*hashtag\/'))
    items = {}
    
    for a in hrefs:
      
        #print(a.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.text)
        #break      
        desc = (a.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.text)
 
        story_fbid = (a['href'].split("%")[0]).split(".")[-1]
        item_id = (a['href'].split(".")[-1]).split("%")[0]
        
        url = "https://m.facebook.com/story.php?story_fbid=%s&id=%s" % (story_fbid, item_id)

        items[url] = desc
    
    #print(posts_list)
    print("Post List Size: %s" % len(items))
    return items

def get_post_content(url):

    print("Post URL: [%s]" % url)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text
    except:
        traceback.print_exc()
        return ""

    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")    
    meta = soup.findAll("meta", {"name":"description"})    
    cont = None   
 
    if meta and 'content' in meta[0].attrs:
        cont = (meta[0]['content'])

    if title:
        #print("title [%s]" % title)
        msg = "<b>%s</b>" % title.text.strip().split("|")[0]
       
        if cont:
            msg = msg + DEL + cont
        print("msg [%s]" % msg)
        return msg
    else:
        return None

def push_posts_list(group, pdict, tg_group, excerpt=False):

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

    for key in pdict:
    
        #'https://m.facebook.com/story.php?story_fbid=4210050162362435&id=223783954322429'
        pid = key.split('=')[-2].split('&')[0]
    
        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            new_posts_list.append(pid)
            url = key
            if (excerpt):
                message = pdict[key] + DEL
                message = message + url
            else:
                message = url
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
            msg  = u'\U0001F4F0' + " <b>Latest Posts Updates</b>" + DEL + msg
        
        print("Msg sent: [%s]" % msg)
        bot_sender.broadcast_list(msg, tg_group)
        
        send_count = send_count + 1

def distribute_posts(grpList, tg_group, isTest=False):

    if (isTest):
        grpList =  wp.repo_facebook('test')
        tg_group = "telegram-chat-test"

    for group in grpList:
        try:
            pdict = get_posts_dict(group[0])
            #print(plist)         
            push_posts_list(group=group[0], pdict=pdict, tg_group=tg_group, excerpt=group[1])
        except:
            print("Error getting post list....")
            traceback.print_exc()
    
def main():

    maintest()
    return

    isTest = not wp.repo_status('facebook') 
    gList = ['notice', 'gwc_global', 'gwc_leisure', 'zerohedge', 'itdog', 'parents', 'leisure', 'ptgroup', 'jetso']
    isTest = False
    
    for channel in gList:
        grpList = wp.repo_facebook(channel)
        tg_group = "telegram-%s" % channel
        distribute_posts(grpList, tg_group, isTest)
        time.sleep(20)
        
        if isTest:
            break

def maintest():

    plist = get_posts_dict('sspgadgetoutlet')
    return

    urls = [#'https://www.facebook.com/unclesiu/posts/761382460874325', 
            'https://www.facebook.com/cablefinance/posts/2195615380489521'
            ]

    for url in urls:
        get_post_content(url)
 
if __name__ == "__main__":
    main()
    #maintest()        
        

