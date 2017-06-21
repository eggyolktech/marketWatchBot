#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time

from market_watch.telegram import bot_sender

CHECK_PERIOD = 60

def get_market_alerts():
    
    url = 'https://rss.dailyfx.com/feeds/alerts'
    print("Url: [" + url + "]")
    passage = ""

    d = feedparser.parse(url)

	# print all posts
    count = 1

    print("\n" + str(datetime.fromtimestamp(time.mktime(gmtime()))))
       	
    for post in d.entries[:10]:
       # get the difference in seconds        
        elapse = time.mktime(gmtime()) - time.mktime(post.published_parsed)
        print("Post #" + str(count) + " - " + post.published + " - " + str(elapse/60) + " mins ago")
        if(elapse/60 <= CHECK_PERIOD):
            passage = passage + "<b>" + post.title + "</b>" + "\n"
            #passage = passage + post.description + "\n"
            passage = passage + "@ " + post.published + "\n\n"
            passage = passage + post.link + "\n\n"
 
        count += 1

    print("Total # of posts processed: %s" % (count-1))
    
    print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():
    passage = get_market_alerts()

    # Send a message to a chat room (chat room ID retrieved from getUpdates)
    if(passage):
        bot_sender.broadcast(passage)

if __name__ == "__main__":
    main()        
        

