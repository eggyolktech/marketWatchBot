#!/usr/bin/python

import shlex
import subprocess
import re
from bs4 import BeautifulSoup

def call_curl(curl):
    args = shlex.split(curl)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8')

def main():
    
    group = 'shensimon'
    #group = 'sspgadgetoutlet'
    
    curl="curl 'https://m.facebook.com/%s/?ref=page_internal' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' -H 'Origin: https://www.example.com' --compressed" % group
    html = call_curl(curl)
    #print(html)
    
    soup = BeautifulSoup(html, "html.parser")
    hrefs = soup.find_all("a", href = re.compile(r".*%s\/\?refid=" % group))
    #hrefs = soup.find_all("a", href = re.compile(r'.*hashtag\/'))
    items = {}
    for a in hrefs:
      
        #print(a.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.text)
        #break      
        desc = (a.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.text)
 
        story_fbid = (a['href'].split("%")[0]).split(".")[-1]
        item_id = (a['href'].split(".")[-1]).split("%")[0]
        
        url = "https://m.facebook.com/story.php?story_fbid=%s&id=%s" % (story_fbid, item_id)

        items[url] = desc
        
    print(items)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



