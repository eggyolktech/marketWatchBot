#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time
import hashlib
import json
from market_watch.telegram import bot_sender

DEL = "\n\n"

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_latest_news_by_code(code, number=10): 

    DEL = "\n\n"
    EL = "\n"

    if (not is_number(code) and is_number(number)):
        print("Code to Quote: [" + code + "]")
        print("Number to Grab: [" + str(number) + "]")
    else:
        return "<i>Usage:</i> " + "/qn" + "[Symbol] (e.g. " + "/qnBABA" + ")"

    url = "https://seekingalpha.com/api/sa/combined/%s.xml" % code.strip()

    print("Url: [" + url + "]")
    passage = ""

    d = feedparser.parse(url)
    
    try:
        ftitle = d['feed']['title']
    except:
        return "No SA news found for %s" % code

    # print all posts
    count = 1

    print("\n" + str(datetime.fromtimestamp(time.mktime(gmtime()))))
       	
    for post in d.entries:

        if ("news?source" in post.link):
            rlink = post.guid.replace("MarketCurrent:","news/")
            passage = passage + "<a href='"+ rlink + "'>" + post.title + "</a> (" + post.published + ")" + DEL
            #print(post.guid)
        count += 1
        if count >= number:
            break

    print("Total # of posts processed: %s" % (count-1))
   
    if (passage):
        passage = u'\U0001F170' + " " + ftitle + DEL + passage
 
    #print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    passage = get_latest_news_by_code("MDB")
    print(passage)
    
    bot_sender.broadcast_list(passage)

if __name__ == "__main__":
    main()        
        

