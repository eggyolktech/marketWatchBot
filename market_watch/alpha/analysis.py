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
    ftitle = d['feed']['title']

    # print all posts
    count = 1

    print("\n" + str(datetime.fromtimestamp(time.mktime(gmtime()))))
       	
    for post in d.entries:
        passage = passage + "<b>" + post.title + "</b> (" + ftitle + ")\n"
        passage = passage + post.description + "\n"
        passage = passage + "Published @ " + post.published + "\n\n"
        passage = passage + post.link + "\n\n"
 	print(post.link)
        count += 1

    print("Total # of posts processed: %s" % (count-1))
    
    #print("Passage: [" + passage + "]")
    #passage = ""
    return passage

def main():

    get_alpha_analytics("BABA")

if __name__ == "__main__":
    main()        
        

