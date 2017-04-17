from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser
import json

config = configparser.ConfigParser()
config.read('config.properties')

from classes.AastocksEnum import TimeFrame, FxCode, IndexCode
from classes.AastocksConstants import *

QQ = "/qq"

def get_qq_command_list(code):

    passage = "Quick Access List for " + code + DEL
    
    if (code == "Fx"):
        for name, member in FxCode.__members__.items():
            passage = passage + QQ + name + EL    
    elif (code == "Index"):
        for name, member in IndexCode.__members__.items():
            passage = passage + QQ + name + EL
    elif (code == "IndexComposite"):
        
        with open('data/list_IndexList.json', encoding="utf-8") as data_file:    
            indexlists = json.load(data_file)    
            
        for indexlist in indexlists:
            passage = passage + QQ + "IC" + indexlist["code"] + " (" + indexlist["label"] + ")" + EL       
    else:
        passage = u'\U000026D4' + ' Service Not Available'
    return passage   

def get_qq_command_detail_list(code):

    passage = "Quick Access Detail List for " + code + DEL
    
    if (code.startswith("IC")):
    
        with open('data/list_IndexList.json', encoding="utf-8") as data_file:    
            indexlists = json.load(data_file)  
        
        indexCode = code.replace("IC", "")
        filtered_index = [x for x in indexlists if x['code'] == indexCode]
        
        for stock in filtered_index[0]["list"]:
            passage = passage + QQ + stock["code"] + " (" + stock["label"] + ")" + EL
        
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

    print(get_qq_command_list("IndexComposite").encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



