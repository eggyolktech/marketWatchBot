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
import hashlib

from market_watch.telegram import bot_sender
from market_watch.util import selenium_helper
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

DEL = "\n\n"
EL = "\n"

NEW_POSTS_COUNT = 45 
GET_POSTS_COUNT = 15

def news_subject(url):
   
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=20)
    r.encoding = "UTF-8"
    html = r.text
    #html = selenium_helper.get_content(url, 3)
    soup = BeautifulSoup(html, "html.parser")
    #time = soup.find("span", {"class": "time"}).text.strip()
    subject = soup.find("span", {"class": "title"}).text.strip()
    
    if subject:
        headsub = subject.replace("【", "").replace("】", "")
        if len(headsub) > 10:
            subject = headsub
    else:
        subject = soup.find("span", {"class": "content"}).text.strip()
        subject = subject.split("丨")[-1]    

    sprint = "Subject (%s)" % (subject)
    print(sprint)
    return subject
 
def news():

    url = "https://m.gelonghui.com/live"
    print("URL: [" + url + "]")  
 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=20)
    r.encoding = "UTF-8"
    html = r.text
    #html = selenium_helper.get_content(url, 3)
    soup = BeautifulSoup(html, "html.parser")

    #print(soup.prettify())
    passages = [] 
    passage = ""
    now = datetime.now()
    
    print("Timestamp now: [" + str(now) + "]")

    lis = soup.find("div", {"class": "live-list-container"}).find_all("div", {"class":"live-card"})
    for li in lis:

        link = li.find("a")
        passageid = link['href'].split("/")[-1]
        content = link.text.strip()
 
        #print([passageid, content])
        
        lurl = "https://m.gelonghui.com/live/%s" % (passageid)
        
        #passage = u'\U0001F3E0' + " <a href='%s'>%s (%s)</a>" % (lurl, subject, timetxt)
        #passage = u'\U0001F3E0' + " <a href='%s'>%s</a>" % (lurl, subject)
        #print("%s - %s (%s)" % (link, passageid, timetxt))
        passages.append((passageid, lurl))

    return passages

def cTime(timetxt):

    try:
        hour = timetxt.split(":")[0]
        mins = timetxt.split(":")[1]
        hkHour = int(hour) + 8
        hkHour = (hkHour - 24) if hkHour > 24 else hkHour
        timetxt = str(hkHour) + ":" + mins
        return timetxt
    except:
        return timetxt 

def main(args):

    passages = news()
    #print(passages)
    #return
    rkey = "NEWS:MGELONGHUI"
    #rkey = "NEWS:MGELONGHUI:TEST"
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
        purl = passage[1]

        if (pid in posts_list):
            print("Post ID [%s] is OLD! Skip sending...." % (pid))
        else:
            print("Post ID [%s] is NEW! Prepare for sending...." % (pid))
            subject = news_subject(purl)
            ptext = u'\U0001F3E0' + " <a href='%s'>%s</a>" % (purl, subject)
            new_posts_list.append(pid)
           
            #bot_sender.broadcast_list(ptext, url_preview=False)  
            bot_sender.broadcast_list(ptext, "telegram-zerohedge", url_preview=False)  
            
            #print("BEFORE Post List %s" % posts_list)
            posts_list = new_posts_list + posts_list
            #print("AFTER Posts List %s" % posts_list)
            #print("AFTER Posts List (Limited) %s" % posts_list[:NEW_POSTS_COUNT])
            new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
            redis_pool.setV(rkey, new_json_arr)

if __name__ == "__main__":
    main(sys.argv)                
              



