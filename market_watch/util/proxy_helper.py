#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import time
import requests
from bs4 import BeautifulSoup
from market_watch.redis import redis_pool
import socket
import random

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

#GOOD_LIST = ['Hong Kong', 'United Kingdom', 'France', 'Japan', 'United States', 'Germany']
GOOD_LIST = ['Hong Kong', 'United Kingdom', 'France', 'Japan', 'Germany']

def check_proxy(proxy_json):

    ip = proxy_json['ip']
    port = proxy_json['port']
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)

    result = s.connect_ex((ip, int(port)))
    if result == 0:
        #print("Port is open")
        return True
    else:
        #print("Port is not open")
        return False

    s.close()

def get_proxy():

    url = "https://www.sslproxies.org/"

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 

    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    rows = soup.find("table", {"id": "proxylisttable"}).find_all('tr')
    proxy_list = []
    
    for row in rows[1:-1]:
        #print(row)
        cols = row.find_all("td")
        country = cols[3].text.strip()
        #print(country)

        if country in GOOD_LIST:
            pjson = {'ip': cols[0].text.strip(), 'port': cols[1].text.strip(), 'country': country}
            #print("%s (%s) - %s" % (pjson, country, " CHECKING...."))
            pcheck = check_proxy(pjson)
            print("%s (%s) - %s" % (pjson, country, pcheck))
 
            if pcheck:
                #return pjson
                proxy_list.append(pjson)

    rp = random.choice(proxy_list)
    print("Chosen proxy: %s" % rp)
    return rp

def push_posts_list(group, plist, tg_group, excerpt=False):

    rkey = "CHUANSONG:" + group
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
        ptitle = "[%s] %s" % (group, post[1])
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

def main():

    p = get_proxy()
    print("Proxy %s" % p)

if __name__ == "__main__":
    main()        
        

