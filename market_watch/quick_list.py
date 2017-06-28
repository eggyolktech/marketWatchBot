#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import json

from market_watch.common.AastocksEnum import TimeFrame, FxCode, IndexCode
from market_watch.common.AastocksConstants import *

QQ = "/qq"

def get_qq_command_list(code):

    passage = "Quick Access List for " + code + DEL
    #QQLIST = {'Fx', 'HKIndexes', 'HKIndexesComposite', 'HKETF', 'HKIndustries', 'USIndexesComposite', 'USETF', 'USIndustries'}
    
    if (code == "Fx"):
        for name, member in FxCode.__members__.items():
            passage = passage + QQ + name + EL    
    elif (code == "HKIndexes"):
        for name, member in IndexCode.__members__.items():
            passage = passage + QQ + name + EL
    elif (code == "HKIndexesComposite"):
        passage = get_json_list_passage(passage, '../data/list_IndexList.json', 'HKIDX')
    elif (code == "HKETF"):
        passage = get_json_list_passage(passage, '../data/list_ETFList.json', 'HKETF')
    elif (code == "HKIndustries"):
        passage = get_json_list_passage(passage, '../data/list_IndustryList.json', 'HKIND')
    elif (code == "USIndexesComposite"):
        passage = get_json_list_passage(passage, '../data/list_USIndexList.json', 'USIDX')  
    elif (code == "USETF"):
        passage = get_json_list_passage(passage, '../data/list_USETFList.json', 'USETF')  
    elif (code == "USIndustries"):        
        passage = get_json_list_passage(passage, '../data/list_USIndustryList.json', 'USIND') 
    else:
        passage = u'\U000026D4' + ' Service Not Available'
    return passage   

def get_json_list_passage(passage, jsonPath, prefix):

    with open(jsonPath, encoding="utf-8") as data_file:    
        indexlists = json.load(data_file)    
        
    for indexlist in indexlists:
        code = indexlist["code"].replace("HKETF", "").replace("USIDX", "").replace("USETF", "").replace("USIND", "") 
        passage = passage + QQ + prefix + code + " (" + indexlist["label"] + ")" + EL  
        
    return passage    

def get_json_list_detail_passage(code, passage, jsonPath, prefix):
    
    with open(jsonPath, encoding="utf-8") as data_file:    
        indexlists = json.load(data_file)  
    
    indexCode = code.replace(prefix, "")
    filtered_index = [x for x in indexlists if x['code'] == indexCode]
    
    if (filtered_index):
        for stock in filtered_index[0]["list"]:
            passage = passage + QQ + stock["code"] + " (" + stock["label"] + ")" + EL
    else:
        passage = u'\U000026D4' + ' List Not Available'
    
    return passage
    
def get_qq_command_detail_list(code):

    passage = "Quick Access Detail List for " + code + DEL
    
    # {'HKIDX', 'HKETF', 'HKIND', 'USIDX', 'USETF', 'USIND'}
    
    if (code.startswith("HKIDX")):
        passage = get_json_list_detail_passage(code, passage, '../data/list_IndexList.json', 'HKIDX')
    elif (code.startswith("HKETF")):            
        passage = get_json_list_detail_passage(code, passage, '../data/list_ETFList.json', 'N-A')
    elif (code.startswith("HKIND")):            
        passage = get_json_list_detail_passage(code, passage, '../data/list_IndustryList.json', 'HKIND')
    elif (code.startswith("USIDX")):            
        passage = get_json_list_detail_passage(code, passage, '../data/list_USIndexList.json', 'N-A')  
    elif (code.startswith("USETF")):            
        passage = get_json_list_detail_passage(code, passage, '../data/list_USETFList.json', 'N-A')  
    elif (code.startswith("USIND")):            
        passage = get_json_list_detail_passage(code, passage, '../data/list_USIndustryList.json', 'N-A')
    else:
        passage = u'\U000026D4' + ' Service Not Available'
        
    return passage       
  
def get_qq_command_tf_list(code):

    passage = "Quick Chart List for " + code + DEL
    passage = passage + "/qM" + code + " (Monthly)" + EL
    passage = passage + "/qw" + code + " (Weekly)" + EL
    passage = passage + "/qd" + code + " (Daily)" + EL
    passage = passage + "/qh" + code + " (Hourly)" + EL
    passage = passage + "/qm" + code + " (Minute)" + EL
    
    return passage
    

def main():

    print(get_qq_command_list("HKIndexesComposite").encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



