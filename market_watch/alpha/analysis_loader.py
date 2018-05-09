#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time
import hashlib
import json
from market_watch.telegram import bot_sender

DEL = "\n\n"

def get_analysis(code):
    
    url = "https://seekingalpha.com/api/sa/combined/%s.xml" % code.strip()

    print("Url: [" + url + "]")
    passage = ""

    d = feedparser.parse(url)
    
    try:
        ftitle = d['feed']['title']
    except:
        return "No SA analysis found for %s" % code

    # print all posts
    count = 1

    print("\n" + str(datetime.fromtimestamp(time.mktime(gmtime()))))
       	
    for post in d.entries:

        if ("article" in post.link):
            passage = passage + "<a href='"+ post.link + "'>" + post.title + "</a> (" + post.published + ")" + DEL

        count += 1

    print("Total # of posts processed: %s" % (count-1))
   
    if (passage):
        passage = u'\U0001F170' + " " + ftitle + DEL + passage
 
    #print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    passage = get_analysis("BABA")
    print(passage)
    print(get_analysis("BA1BA"))
    
    bot_sender.broadcast_list(passage)

if __name__ == "__main__":
    main()        
        

