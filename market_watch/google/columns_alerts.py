#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time
import urllib.parse as urlparse 

from market_watch.telegram import bot_sender

def get_columns_alerts(url):
    
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
        #if(elapse/60 <= CHECK_PERIOD):
        print(post.title.encode('utf-8'))
        #return
        passage = passage + "" + str(post.title) + "" + "\n"

        #passage = passage + post.description + "\n"
        passage = passage + "@ " + post.published + "\n\n"

        actuallink = urlparse.parse_qs(post.link)['url'][0]
        passage = passage + actuallink + "\n\n"
 
        count += 1

    print("Total # of posts processed: %s" % (count-1))
    
    print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    #columns = ['https://www.google.com.hk/alerts/feeds/17097742724167324955/8551375453331312334', 'https://www.google.com.hk/alerts/feeds/17097742724167324955/12218577883122648771','https://www.google.com.hk/alerts/feeds/17097742724167324955/14866853673326524888']
    columns = [
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/12218577883122648771', # winson
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/6235280641080477545', #choi kam 
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/12185381887594353633', # lam boon
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/3555398835609438380', # fu hoi
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/3555398835609440167', # leung chung
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/15712087392887966231', # ivan li
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/6954474239905041744', # chow hin 
            'https://www.google.com.hk/alerts/feeds/17097742724167324955/2752388232462749823', # shum wing lin
            'https://www.google.com/alerts/feeds/17097742724167324955/2656866248812261984', # tang kin chor
            ]
    
    for colurl in columns:    
        passage = get_columns_alerts(colurl)
        # Send a message to a chat room (chat room ID retrieved from getUpdates)
        if(passage):
            bot_sender.broadcast(passage)

if __name__ == "__main__":
    main()        
        

