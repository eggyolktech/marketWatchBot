#!/usr/bin/python

from pymongo import MongoClient
from market_watch.util import config_loader

import datetime
import json

config = config_loader.load()
conn_str = config.get("mongodb", "connection")
client = MongoClient(conn_str)
db = client.marketwatch

def repo_twitter(channel):
    res = []
    fres = db.twitter.find({"channel":channel}, {"_id":0, "feeds":1})
    fres = fres[0] if fres.count() == 1 else {}

    if 'feeds' in fres:
        for acc in fres['feeds']:
            if acc['active']:
                res.append(acc['username'])        
    return res

def repo_rss(channel):
    res = []
    fres = db.rss.find({"channel":channel}, {"_id":0, "feeds":1})
    fres = fres[0] if fres.count() == 1 else {}
    
    if 'feeds' in fres:
        for acc in fres['feeds']:
            if acc['active']:
                res.append(acc['url'])        
    return res

def repo_facebook(channel):
    res = []
    fres = db.facebook.find({"channel":channel}, {"_id":0, "feeds":1})
    fres = fres[0] if fres.count() == 1 else {}

    if 'feeds' in fres:
        for acc in fres['feeds']:
            if acc['active']:    
                res.append((acc['username'], True))        
    return res

def repo_status(category):

    control = db.control.find_one({})
    #print(control)
    if category in control:
        return control[category]
    else:
        return False

if __name__ == "__main__":

    print("Test")

    #print("Repo Status: %s" % repo_status('facebook'))

    for l in ["notice", "parents", "itdog", "leisure", "test"]:
        print("\n==== FB Feed %s\n%s" % (l, repo_facebook(l)))

    for l in ["notice", "itdog", "test"]:
        print("\n==== RSS Feed %s\n%s" % (l, repo_rss(l)))

    for l in ["twitter", "zerohedge", "itdog", "leisure", "test"]:
        print("\n==== Twitter Feed %s\n%s" % (l, repo_twitter(l)))


