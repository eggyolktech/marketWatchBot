#!/usr/bin/python

import twitter
import time
import sys
import os
from market_watch.util import config_loader
from market_watch.telegram import bot_sender
from market_watch.redis import redis_pool
import json

config = config_loader.load()

DEL = '\n\n'
NEW_TWEET_COUNT = 30
GET_TWEET_COUNT = 10

API = twitter.Api(consumer_key=config.get("twitter","consumer_key"),
                    consumer_secret=config.get("twitter","consumer_secret"),
                    access_token_key=config.get("twitter","access_token_key"),
                    access_token_secret=config.get("twitter","access_token_secret"),
                    tweet_mode='extended')

def push_tweet(name, tcount=1):

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
        statuses = API.GetUserTimeline(screen_name=sname, count=get_count)
    except:
        print("User Timeline Error: [%s]" % name)
        return

    messages_list = []
    
    for s in statuses:
        if (str(s.id) in tweet_list):
            print("%s created at %s is OLD! Skip sending...." % (s.id, s.created_at))
        else:
            print("%s created at %s is NEW! Prepare for sending...." % (s.id, s.created_at))
            tweet_list.append(str(s.id))
            url = ('https://mobile.twitter.com/i/web/status/%s' % s.id)
            created = (s.created_at)
            text = (s.full_text)        
            message = "%s\n(<a href='%s'>%s</a>)" % (text, url, created)
            messages_list.append(message)

    tweet_list.sort(reverse=True)
    print("Full Tweet List %s" % tweet_list[:NEW_TWEET_COUNT])
    new_json_arr = json.dumps(tweet_list[:NEW_TWEET_COUNT])
    redis_pool.setV(rkey, new_json_arr)    

    if messages_list:
        messages_list.insert(0, u'\U0001F30F' + "<b>@%s is Tweeting...</b>" % name)
        full_message = DEL.join(messages_list)
        #bot_sender.broadcast_list(full_message)
        bot_sender.broadcast_list(full_message, "telegram-notice")
    
def get_tweet(name, tcount=1):

    #user = API.GetUser(screen_name='@realDonaldTrump')
    #print(user)
    #print("UserImg %s" % user.profile_image_url)
    
    sname = '@%s' % name
    statuses = API.GetUserTimeline(screen_name=sname, count=tcount)    
    messages_list = []

    for s in statuses:    
        url = ('https://mobile.twitter.com/i/web/status/%s' % s.id)
        created = (s.created_at)
        text = (s.full_text)        
        message = "%s\n(<a href='%s'>%s</a>)" % (text, url, created)
        messages_list.append(message)
    
    full_message = "No tweets were found!"
    
    if messages_list:
        messages_list.insert(0, u'\U0001F30F' + "<b>Latest Tweets for @%s</b>" % name)
        full_message = DEL.join(messages_list)
    
    print("Message: [%s]" % full_message)
    return full_message

def trump(tcount=1):
    return get_tweet('realDonaldTrump', tcount)

def main(args):
    
    start_time = time.time()

    if (len(args) > 1 and args[1] == "push_tweet"):
        WATCHER = ['realDonaldTrump','usstockcaptain','RayDalio', 'webbhk', 'muddywatersre', 'stocktwits']
        #WATCHER = ['realDonaldTrump']
        for w in WATCHER:
            push_tweet(w)
    else:
        trump(5)
    
    print("Time elapsed: " + "%.3f" % (time.time() - start_time) + "s")    

if __name__ == "__main__":
    main(sys.argv)  
