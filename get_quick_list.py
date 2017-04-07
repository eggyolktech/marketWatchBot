from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

from classes.AastocksEnum import TimeFrame, FxCode, IndexCode
from classes.AastocksConstants import *

QQ = "/qq"

def get_qq_command_list(code):


    passage = ""
    QQLIST = {'Fx', 'Index', 'ETF', 'Bluechip', 'Industry'}
    
    if (code == "Fx"):
        passage = "Quick Access List for " + code + DEL
        for name, member in FxCode.__members__.items():
            passage = passage + QQ + name + EL    
    elif (code == "Index"):
        passage = "Quick Access List for " + code + DEL
        for name, member in IndexCode.__members__.items():
            passage = passage + QQ + name + EL
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

    print(get_latest_news_by_code("939", 5).encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



