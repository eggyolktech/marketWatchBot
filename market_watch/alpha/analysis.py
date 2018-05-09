#!/usr/bin/python

import feedparser
from time import gmtime
from datetime import datetime
import time
import hashlib
import json

CHECK_PERIOD = 70
NEW_POSTS_COUNT = 20
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_alpha_analytics(code):
    
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
            passage = passage + "<b>" + "<a href='"+ post.link + "'>" + post.title + "</a>" + "</b> (" + post.published + ")" + DEL

        count += 1

    print("Total # of posts processed: %s" % (count-1))
   
    if (passage):
        passage = passage + u'\U0001F170' + " " + ftitle + DEL
 
    #print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    print(get_alpha_analytics("BABA"))
    print(get_alpha_analytics("BA1BA"))

if __name__ == "__main__":
    main()        
        

