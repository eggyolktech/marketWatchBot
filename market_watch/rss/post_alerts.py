#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time

from market_watch.telegram import bot_sender

CHECK_PERIOD = 60

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
            passage = passage + "<b>" + post.title + "</b> (" + ftitle + ")\n"
            #passage = passage + post.description + "\n"
            passage = passage + "Published @ " + post.published + "\n\n"
            passage = passage + post.link + "\n\n"
 
        count += 1

    print("Total # of posts processed: %s" % (count-1))
    
    print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    RSS_REPO = ['http://oldjimpacific.blogspot.com/feeds/posts/default', 'https://medium.com/feed/@ivansyli', 'http://feeds.feedburner.com/bituzi']
    #RSS_REPO = ['https://medium.com/feed/@ivansyli', 'http://feeds.feedburner.com/bituzi']
    
    for rss in RSS_REPO:
        passage = get_rss_alerts(rss)

        if(passage):
            print(passage)
            #bot_sender.broadcast_list(passage)
            bot_sender.broadcast_list(passage, "telegram-notice")

if __name__ == "__main__":
    main()        
        

