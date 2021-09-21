#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time
import hashlib
import json
import traceback
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool
from market_watch.mongodb import watcher_repo as wp

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
    #print("posts [%s]" % posts)
    url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
    ftitle = posts['feed']['title'] if 'title' in posts['feed'] else ""
    
    rkey = "RSS:" + str(url_hash)
    json_arr = redis_pool.getV(rkey)
    posts_list = []    

    if (json_arr):
        print("Posts Redis Cache exists for [%s] [%s]" % (url, rkey))
        json_arr = json_arr.decode()        
        posts_list = json.loads(json_arr)
        print("Loaded Posts List %s" % posts_list)
        get_count = GET_POSTS_COUNT  
    else:
        get_count = NEW_POSTS_COUNT
       
    for post in posts.entries[:get_count]:
   
        #print(post.keys())

        if 'published_parsed' in post.keys(): 
            stime = str(time.mktime(post.published_parsed))
        else:
            stime = str(time.mktime(post.updated_parsed))

        stitle = post.title
        if "ERROR WHILE FETCHING" in stitle:
            print(stitle)
            return
        
        if (str(stime) in posts_list):
            print("Post created at %s is OLD! Skip sending...." % (stime))
        else:
            print("Post created at %s is NEW! Prepare for sending...." % (stime))
            new_posts_list.append(stime)
            #message = post.link
            message = "<b>" + stitle + "</b>\n"
            message = message + post.link
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
            #passage = passage + "<b>" + post.title + "</b>\n"
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
            #if 'lpt' in tg_group or 'zerohedge' in tg_group:
            if 'lpt' in tg_group:
                bot_sender.broadcast_list(passage, tg_group, False)
            else:
                bot_sender.broadcast_list(passage, tg_group)

def main():

    isTest = not wp.repo_status('rss') 
    
    if (isTest):
        repoList = wp.repo_rss('test')
        tg_group = "telegram-chat-test"   
        push_rss(repoList, tg_group)
        return

    for repo in ['zerohedge', 'notice', 'itdog', 'lpt', 'gwc_leisure', 'parents']:
    #for repo in ['lpt']:
        repoList = wp.repo_rss(repo)
        tg_group = "telegram-%s" % repo
        push_rss(repoList, tg_group)


if __name__ == "__main__":
    main()        

