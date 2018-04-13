#!/usr/bin/python

import twitter
import os
from market_watch.util import config_loader

config = config_loader.load()

MAX_MSG_SIZE = 4096
DEL = '\n\n'

def trump(tcount=1):

    api = twitter.Api(consumer_key=config.get("twitter","consumer_key"),
                        consumer_secret=config.get("twitter","consumer_secret"),
                        access_token_key=config.get("twitter","access_token_key"),
                        access_token_secret=config.get("twitter","access_token_secret"),
                        tweet_mode='extended')
    
    statuses = api.GetUserTimeline(screen_name='@realDonaldTrump', count=tcount)
    
    messages_list = []
    
    for s in statuses:        
        url = ('https://twitter.com/i/web/status/%s' % s.id)
        created = (s.created_at)
        text = (s.full_text)        
        message = "%s (%s) - <a href='%s'>Open</a>" % (text, created, url)
        messages_list.append(message)
    
    full_message = "You are Fired!! (No tweets)"
    
    if messages_list:
        full_message = DEL.join(messages_list)
    
    print("Trump Message: [%s]" % full_message)
    return full_message

def main():

    trump(10)
    
if __name__ == "__main__":
    main() 
