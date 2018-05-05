#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time

from market_watch.telegram import bot_sender

CHECK_PERIOD = 70 

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
    
    print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    RSS_REPO = ['http://oldjimpacific.blogspot.com/feeds/posts/default', 
                'https://medium.com/feed/@ivansyli', 
                'http://feeds.feedburner.com/bituzi', 
                'http://fb2rss.altervista.org/?id=193368377704187', #平行時空：沈旭暉國際學術新聞台 
                'http://fb2rss.altervista.org/?id=1744632715750914', #Ivan Li 李聲揚 - 華麗后台
                'http://fb2rss.altervista.org/?id=223783954322429', #堅離地城：沈旭暉國際生活台 Simon's Glocal World
                'http://fb2rss.altervista.org/?id=393581457698786', #萬國郵政 Simon's Stamps International
                'http://fb2rss.altervista.org/?id=128674903851093', #Dr Lam
                'http://fb2rss.altervista.org/?id=247333838767466', #張士佳 - Sky Sir
                'http://fb2rss.altervista.org/?id=112243028856273', #英之見 - 基金經理黃國英Alex Wong
                'http://fb2rss.altervista.org/?id=767813843325038', #Eddie Team
                ]
    #RSS_REPO = ['https://medium.com/feed/@ivansyli', 'http://feeds.feedburner.com/bituzi']
    
    for rss in RSS_REPO:
        passage = get_rss_alerts(rss)

        if(passage):
            print(passage)
            #bot_sender.broadcast_list(passage)
            bot_sender.broadcast_list(passage, "telegram-notice")

if __name__ == "__main__":
    main()        
        

