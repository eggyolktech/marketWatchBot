#!/usr/bin/python

import json
import traceback
import logging

QT = "/qt"
EL = "\n"
HK_FILE = "/app/hickoryStratsWatcher/web/json/hkTrackList.json"
US_FILE = "/app/hickoryStratsWatcher/web/json/usTrackList.json"

def init_track(region="HK"):
    
    # empty dictionary
    data = {}
    dump_dict(data, get_file(region))

def get_file(region="HK"):

    path = HK_FILE
    if (region == "US"):
        path = US_FILE

    return path 

def add_track(code):

    data = None
    region = None
    
    print("Code to Add: [" + code + "]")
    
    try:
        if (not code):
            return False
        elif (is_number(code)):
            data = load_dict("HK")
            data[code] = code + ".HK"
            region = "HK"
        else:
            data = load_dict("US")
            if (not ".US" in code):
                code = code + ".US"
            data[code.upper()] = code.upper()
            region = "US"
        
        if (data and region):
            print(data)
            dump_dict(data, get_file(region))
            
        return True
        
    except:
        logging.error(traceback.format_exc())
        return False

def list_track():

    d1 = load_dict("HK")
    d2 = load_dict("US")
    m = ""
    if (d1.items):
        m = "[HK Track List]" + EL
        for key, value in sorted(d1.items()):
            m = m + (key + " - " + "/qd" + value.replace(".HK","")) + EL
    
    if (d2.items):
        m = m + EL + "[US Track List]" + EL
        for key, value in sorted(d2.items()):
            m = m + (key.replace(".US","") + " - " + "/qd" + value.replace(".US","")) + EL
    
    if (not m):
        m = "No Data"
    
    return m
  
def dump_dict(data, file):

    with open(file, 'w') as fp:
        json.dump(data, fp)
   
def load_dict(region="HK"):
    
    file = HK_FILE
    if (region == "US"):
        file = US_FILE

    with open(file, 'r') as fp:
        data = json.load(fp)
        return data

def remove_track(code):

    data = None
    region = None
    
    print("Code to Remove: [" + code + "]")
    
    try:
        if (not code):
            return False
        elif (is_number(code)):
            data = load_dict("HK")
            if code in data:
                del data[code]
            else:
                print("No key found!")
                return False
            region = "HK"
        else:
            data = load_dict("US")
            
            if (not ".US" in code):
                code = code + ".US"        
            
            if code.upper() in data:
                del data[code.upper()]
            else:
                print("No key found!")
                return False
            region = "US"
        
        if (data and region):
            dump_dict(data, get_file(region))
    
        return True
    except:
        logging.error(traceback.format_exc())
        return False
 
def main():

    init_track("HK")
    init_track("US")
    #print(load_file("HK"))
    add_track("3800")
    add_track("2628")
    add_track("BABA")
    add_track("GOOG")
    add_track("FB")
    print(list_track())
    remove_track("2628")
    remove_track("939")
    remove_track("FB")
    remove_track("AMZN")
    print(list_track())

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



