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

def get_post_content(url):

    print("Post URL: [%s]" % url)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")    
    
    if title:
        msg = title.text.strip().split("-")[0]
        return msg
    else:
        return None

def push_posts_list(group, plist, tg_group, excerpt=False):

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
            url = "https://www.facebook.com/%s/posts/%s" % (group, pid)
            if (excerpt):
                message = get_post_content(url) + DEL
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
        grpList = [
                    #('Brian.DTHSF', True),
                    #('101121253309673', True),
                    ('Leesimon.hk', True),
                    ]
        tg_group = "telegram-chat-test"

    for group in grpList:
        plist = get_posts_list(group[0])
        push_posts_list(group=group[0], plist=plist, tg_group=tg_group, excerpt=group[1])

    
def main():

    isTest = False 

    grpList = [
                ('ivanliresearch', False), #Ivan Li 李聲揚 - 華麗后台
                ('DrLamInv', False), #Dr Lam
                ('sky788', False), #張士佳 - Sky Sir
                ('112243028856273', True), #英之見 - 基金經理黃國英Alex Wong
                ('1906376359381666', True),
                ('eddietamcai', True), #Eddie Team
                ('Leesimon.hk', True),
                ('thinkingweb', False),
                ('Starmancapital', False), #Starman 資本攻略
                ('Brian.DTHSF', True),
                ('CaptainHK80', True),
                ('101121253309673', True),
                ('GreenHornFans', True),
                #('macandmic', True), #Chan Tai Wai
                #('EdwinNetwork', True),
                ('Investopedia', True),
                #('microchow', True),
                ('muddydirtywater', True),
                ('speculatorjunior', True),
                ('advanceguy1', True),
                ('landmarkreporter', True),
                ('203829452994495', True), #Oldjim
                ('2012jason', True), #Ngai Nick
                ('bituzi', True),
                ('rainingmanhk', True),
                ('stockwing1', True),
                ('cablefinance', True),
                #('p.outlook', True),
                ('stockfarmerhk', True),
                ]
    tg_group = "telegram-notice"
    distribute_posts(grpList, tg_group, isTest)

    grpList = [
                ('mshktech', False), #Microsoft HK Technical Community
                #('therootshk', False),
                ('fuklopedia', True),
                ('itdogcom', True),
                ]
    tg_group = "telegram-itdog"
    distribute_posts(grpList, tg_group, isTest)
    
    grpList = [
                #('parentingtw', False),
                ('hk01parenting', False),
                ('ohpamahk', False),
                ('mphappypama', False), 
                ('378287442642919', True),
                ('JollyKingdom', True),
                ('rightalent', True),
                ('unclesiu', True),
                ('eztalk', True),
                ('popachannel', True),
                ]
    tg_group = "telegram-parents"
    distribute_posts(grpList, tg_group, isTest)

    grpList = [
                ('SimonIRBasilica', True), #平行時空：沈旭暉國際學術新聞台
                ('shensimon', True), #堅離地城：沈旭暉國際生活台 Simon's Glocal World
                ('SimonStamps', True), #萬國郵政 Simon's Stamps International
                ('tokit.channel', False),
                ('gushi.tw', True),
                ('learn.english.free', True),
                ('mamaigo', True),
                ('Cuson.LoChiKong', True),
                ]
    tg_group = "telegram-leisure"
    distribute_posts(grpList, tg_group, isTest)
 
if __name__ == "__main__":
    main()        
        

