#!/usr/bin/python

import twitter
import time
import sys
import os
import re
import random
from market_watch.util import config_loader
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool
import json

config = config_loader.load()

DEL = '\n\n'
NEW_TWEET_COUNT = 30 
GET_TWEET_COUNT = 10

LOADING = [u'\U0000231B', u'\U0001F6AC', u'\U0001F37B', u'\U0001F377', u'\U000023F3', u'\U0000231A', u'\U0001F30F']

API = twitter.Api(consumer_key=config.get("twitter","consumer_key"),
                    consumer_secret=config.get("twitter","consumer_secret"),
                    access_token_key=config.get("twitter","access_token_key"),
                    access_token_secret=config.get("twitter","access_token_secret"),
                    tweet_mode='extended')

def push_tweet(name, tcount=1, test=False, group="telegram-twitter"):

    sname = '@%s' % name
    rkey = "Twitter:" + name.lower()
    json_arr = redis_pool.getV(rkey)
    tweet_list = []    
    
    if (json_arr):
        print("Twitter Redis Cache exists for [%s]" % name)
        json_arr = json_arr.decode()        
        tweet_list = json.loads(json_arr)
        print("Loaded Tweet List %s" % tweet_list)
        get_count = GET_TWEET_COUNT  
    else:
        get_count = NEW_TWEET_COUNT
      
    try:
        statuses = API.GetUserTimeline(screen_name=sname, include_rts=True, exclude_replies=True, count=get_count)
    except:
        print("User Timeline Error: [%s]" % name)
        return

    messages_list = []
    new_tweet_list = []
    for s in statuses:
        if (str(s.id) in tweet_list):
            print("%s created at %s is OLD! Skip sending...." % (s.id, s.created_at))
        else:
            print("%s created at %s is NEW! Prepare for sending...." % (s.id, s.created_at))
            new_tweet_list.append(str(s.id))
            url = ('https://mobile.twitter.com/i/web/status/%s' % s.id)
            created = str(s.created_at)
            text = re.sub(r"\$([A-Za-z]+)",r"/qd\1", s.full_text)
            message = "%s\n(<a href='%s'>%s</a>)" % (text, url, "Post@ " + created.split('+')[0] + "GMT")
            messages_list.append(message)

    
    print("BEFORE Tweet List %s" % tweet_list)
    tweet_list = new_tweet_list + tweet_list
    print("AFTER Tweet List %s" % tweet_list)
    print("AFTER Tweet List (LIMIT) %s" % tweet_list[:NEW_TWEET_COUNT])
    new_json_arr = json.dumps(tweet_list[:NEW_TWEET_COUNT])
    redis_pool.setV(rkey, new_json_arr)    

    if messages_list:
        messages_list.insert(0, "<pre>\n</pre>" + random.choice(LOADING) + "<b>@%s is Tweeting...</b>" % name)
        full_message = DEL.join(messages_list)

        if (test):
            bot_sender.broadcast_list(full_message)
        else:
            bot_sender.broadcast_list(full_message, group) 
    
def get_tweet(name, tcount=1):

    #user = API.GetUser(screen_name='@realDonaldTrump')
    #print(user)
    #print("UserImg %s" % user.profile_image_url)
    
    sname = '@%s' % name
    statuses = API.GetUserTimeline(screen_name=sname, include_rts=True, exclude_replies=True, count=tcount)    
    messages_list = []

    for s in statuses:    
        url = ('https://mobile.twitter.com/i/web/status/%s' % s.id)
        created = str(s.created_at)
        text = re.sub(r"\$([A-Za-z]+)",r"/qd\1", s.full_text)
        message = "%s\n(<a href='%s'>%s</a>)" % (text, url, "Post@ " + created.split('+')[0] + "GMT")
        messages_list.append(message)
    
    full_message = "No tweets were found!"
    
    if messages_list:
        messages_list.insert(0, "<pre>\n</pre>" + random.choice(LOADING) + "<b>Latest Tweets for @%s</b>" % name)
        full_message = DEL.join(messages_list)
    
    print("Message: [%s]" % full_message)
    return full_message

def trump(tcount=1):
    return get_tweet('realDonaldTrump', tcount)

def main(args):
    
    start_time = time.time()
    isTest = False

    if (len(args) > 1 and args[1] == "push_tweet"):
        WATCHER = ['realDonaldTrump',
                    'usstockcaptain', 
                    #'webbhk', 
                    #'muddywatersre', 
                    'stocktwits', 
                    'citronresearch', 
                    'sjosephburns', 
                    #'RRGresearch', 
                    #'RyanDetrick'
                    'alsabogal',
                    'tradeciety',
                    'sunrisetrader',
                    'rayner_teo',
                    'AsennaWealth',
                    'topdowncharts',
                    'AmyAtrade',
                    'barronsonline',
                    'raydalio',
                    'tradingsim',
                    #'zerohedge',
                    ]
        if isTest:
            WATCHER = ['tradingsim']

        for w in WATCHER:
            push_tweet(w, test=isTest)

        WATCHER = ['zerohedge']

        for w in WATCHER:
            push_tweet(w, group="telegram-twitter-zerohedge")

    else:
        get_tweet('sjosephburns', 15)
    
    print("Time elapsed: " + "%.3f" % (time.time() - start_time) + "s")    

if __name__ == "__main__":
    main(sys.argv)  
