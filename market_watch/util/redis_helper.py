#!/usr/bin/python

from time import gmtime
from datetime import datetime
import json
import time
import requests
from bs4 import BeautifulSoup
from market_watch.redis import redis_pool
import socket
import random

NEW_POSTS_COUNT = 25
GET_POSTS_COUNT = 10 
DEL = "\n\n"

def get_new_key_list(rkey, keylist, get_count=20, dryrun=False):

    json_arr = redis_pool.getV(rkey)
    rkeys_list = []    
    messages_list = []
    new_keys_list = []   
 
    if (json_arr):
        print("Posts Redis Cache exists for [%s]" % rkey)
        json_arr = json_arr.decode()        
        rkeys_list = json.loads(json_arr)
        print("Loaded Rkeys List %s" % rkeys_list)

    for key in keylist[:get_count]:

        if (key in rkeys_list):
            print("Key ID [%s] is OLD! Skip sending...." % (key))
        else:
            print("Post ID [%s] is NEW! Add to new key list...." % (key))
            new_keys_list.append(key)
            
    print("BEFORE Post List %s" % rkeys_list)
    rkeys_list = new_keys_list + rkeys_list
    print("AFTER Posts List %s" % rkeys_list)
    print("AFTER Posts List (Truncated) %s" % rkeys_list[:get_count])
    new_json_arr = json.dumps(rkeys_list[:get_count])

    if (not dryrun):
        redis_pool.setV(rkey, new_json_arr)         
    
    return new_keys_list

def main():

    rkey = "TEST:GROUP"
    keylist = ['4', '3', '1','2']

    p = get_new_key_list(rkey, keylist, 2)
    print(p)

if __name__ == "__main__":
    main()        
        

