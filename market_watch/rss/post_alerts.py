#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time
import hashlib
import json

from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool

CHECK_PERIOD = 70
NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_rss_alerts_with_redis(url):
    
    print("Url: [" + url + "]")
    full_message = ""
    messages_list = []
    new_posts_list = []

    posts = feedparser.parse(url)
    url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
    ftitle = posts['feed']['title']
    
    rkey = "RSS:" + str(url_hash)
    json_arr = redis_pool.getV(rkey)
    posts_list = []    

    if (json_arr):
        print("Posts Redis Cache exists for [%s]" % url)
        json_arr = json_arr.decode()        
        posts_list = json.loads(json_arr)
        print("Loaded Posts List %s" % posts_list)
        get_count = GET_POSTS_COUNT  
    else:
        get_count = NEW_POSTS_COUNT
       
    for post in posts.entries[:get_count]:
    
        stime = str(time.mktime(post.published_parsed))
        stitle = post.title
        if "ERROR WHILE FETCHING" in stitle:
            print(stitle)
            return
        
        if (str(stime) in posts_list):
            print("Post created at %s is OLD! Skip sending...." % (stime))
        else:
            print("Post created at %s is NEW! Prepare for sending...." % (stime))
            new_posts_list.append(stime)
            message = post.link
            messages_list.append(message)

    #print("New Posts List %s" % posts_list)
    posts_list = new_posts_list + posts_list
    print("Full Posts List %s" % posts_list[:NEW_POSTS_COUNT])
    new_json_arr = json.dumps(posts_list[:NEW_POSTS_COUNT])
    redis_pool.setV(rkey, new_json_arr)    

    if messages_list:
        messages_list.insert(0, "<pre>\n</pre>" + u'\U0001F4F0' + " <b>Latest Posts Updates</b>")
        full_message = DEL.join(messages_list)

    #print("Passage: [" + full_message + "]")
    return full_message

def get_rss_alerts(url):
    
    print("Url: [" + url + "]")
    passage = ""

    d = feedparser.parse(url)
    ftitle = d['feed']['title']

	# print all posts
    count = 1

    print("\n" + str(datetime.fromtimestamp(time.mktime(gmtime()))))
       	
    for post in d.entries[:10]:
       # get the difference in seconds        
        elapse = time.mktime(gmtime()) - time.mktime(post.published_parsed)
        print("Post #" + str(count) + " - " + post.published + " - " + str(elapse/60) + " mins ago")
        if(elapse/60 <= CHECK_PERIOD):
            #passage = passage + "<b>" + post.title + "</b> (" + ftitle + ")\n"
            #passage = passage + post.description + "\n"
            #passage = passage + "Published @ " + post.published + "\n\n"
            passage = passage + post.link + "\n\n"
 
        count += 1

    print("Total # of posts processed: %s" % (count-1))
    
    #print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def push_rss(repo_list, tg_group):

    for rss in repo_list:
        passage = get_rss_alerts_with_redis(rss)

        if(passage):
            print(passage)
            bot_sender.broadcast_list(passage, tg_group)

def main():

    repoList = ['http://oldjimpacific.blogspot.com/feeds/posts/default', 
                'https://medium.com/feed/@ivansyli', 
                'http://feeds.feedburner.com/bituzi', 
                #'http://fb2rss.altervista.org/?id=1744632715750914', #Ivan Li 李聲揚 - 華麗后台
                #'http://fb2rss.altervista.org/?id=128674903851093', #Dr Lam
                #'http://fb2rss.altervista.org/?id=247333838767466', #張士佳 - Sky Sir
                #'http://fb2rss.altervista.org/?id=112243028856273', #英之見 - 基金經理黃國英Alex Wong
                #'http://fb2rss.altervista.org/?id=767813843325038', #Eddie Team
                'http://hkstockinvestment.blogspot.com/feeds/posts/default', #偉哥投資手札
                'https://parisvalueinvesting.blogspot.com/feeds/posts/default', #巴黎的價值投資
                'https://happyvalleyjockey.blogspot.com/feeds/posts/default', #巴黎的價值投資
                'http://www.justacafe.com/feeds/posts/default', #Just a Cafe
                'http://kenjinrong.com/feed/', #Kenjinrong
                'http://blog.sina.com.cn/rss/1182426800.xml', #陶冬的博客
                #'http://fb2rss.altervista.org/?id=974946689232967' #Starman 資本攻略
                ]
    
    isTest = False
    tg_group = "telegram-notice" 
    
    if (isTest):
        repoList = ['http://feed.tw.wxwenku.com/a/4153/feed', ]
        tg_group = "telegram-chat-test"   

    push_rss(repoList, tg_group)

    if isTest:
        return

    repoList = [#'http://fb2rss.altervista.org/?id=193368377704187', #平行時空：沈旭暉國際學術新聞台
                #'http://fb2rss.altervista.org/?id=223783954322429', #堅離地城：沈旭暉國際生活台 Simon's Glocal World
                #'http://fb2rss.altervista.org/?id=393581457698786', #萬國郵政 Simon's Stamps International
                #'http://fb2rss.altervista.org/?id=713511925511617', #Glollege放眼
                'http://feed.tw.wxwenku.com/a/4153/feed', #Kenjinrong (new)
                'https://www.finlab.tw/atom.xml', #回測與選股教學部落格
                'http://feed.tw.wxwenku.com/a/326/feed', #混子曰
                #'http://fb2rss.altervista.org/?id=246310051900', #Microsoft HK Technical Community
                ]

    tg_group = "telegram-itdog"
    push_rss(repoList, tg_group)


if __name__ == "__main__":
    main()        

