#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

from market_watch.common.AastocksEnum import TimeFrame, FxCode, IndexCode


def get_hkg_chart_list_by_type(code, action, params):
    
    url_dict_list = []
    ind_params = []
    
    for p in params:
        pl = p.lower()
        if (pl == "bb" or pl == "sma" or pl == "night"):
            ind_params.append(pl)

    url_dict_list.append({'code': code, 'url': get_hkg_chart_by_type(code, action, ind_params)})
    
    for p in params:
        if (not p == "bb" and not p == "sma" and not p == "night"):
            url_dict_list.append({'code': p, 'url': get_hkg_chart_by_type(p, action, ind_params)})
    
    return url_dict_list

def get_finvinz_chart(code, period):

    if (period == "M"):
        p = "m1"
    elif (period == "m"):
        p = "m5"
    else:
        p = period + "1"

    return "https://finviz.com/fut_chart.ashx?t=DX&cot=098662&p=%s" % p

def get_hkg_chart_by_type(code, action, params):

    url = ""
    is_bb = False
    is_ema = False
    is_sma = False
    is_night = False
    is_ahft = False
    is_num = False
    is_CN = False
    is_US = False
    is_FX = False
    
    for p in params:
        if (p.lower() == "bb"):
            is_bb = True
        elif (p.lower() == "sma"):
            is_sma = True
        elif (p.lower() == "night"):
            is_night = True
    
    # Determine which code type base on input format
    is_num = is_number(code)
    
    if (is_num and len(code) == 6 and code[:1] == "6"):
        code = code + ".SH"
        is_CN = True
    elif (is_num and len(code) == 6):
        code = code + ".SZ"
        is_CN = True
    elif (is_num):
        code = code + ".HK"    
    elif (code.isalpha()):

        if ("USD" == code.upper()):
            return get_finvinz_chart(code, action)

        if (code.upper() in ["HSIF", "HSIFN", "MHSIF", "MHSIFN"] and is_night):
            is_ahft = True
            
        code = get_aastocks_alpha_code(code)
        
        if (".US" in code):
            is_US = True
        elif (code[:1] == "9"):
            is_FX = True
    else:
        code = "110000.HK"    
    
    # Determine time frame to use base on code type
    timeframe = TimeFrame.DAILY
    
    if (action == "M"):
        if (is_US or is_CN):
            timeframe = TimeFrame.MONTHLYSHORT
        else:
            timeframe = TimeFrame.MONTHLY
    elif (action.lower() == "w"):
        timeframe = TimeFrame.WEEKLY
    elif (action.lower() == "d"):
        timeframe = TimeFrame.DAILY
    elif (action.lower() == "h"):
        if (is_FX):
            timeframe = TimeFrame.HOURLYSHORT
        else:
            timeframe = TimeFrame.HOURLY
    elif (action.lower() == "m"):
        if (is_FX):
            timeframe = TimeFrame.MINUTESHORT
        else:
            timeframe = TimeFrame.MINUTE
    
    main = "http://charts.aastocks.com/servlet/Charts?fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&chart=left&type=1"
    
    
    #indicator = "&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
    indicator= "&Indicator=3&indpara1=10&indpara2=20&indpara3=50&indpara4=100&indpara5=250"
    
    if (is_bb):
        indicator = "&Indicator=9&indpara1=20&indpara2=2&indpara3=0&indpara4=0&indpara5=0"
    if (is_sma):
        indicator = "&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
    
    if (is_ahft):
        ahft_param = "&AHFT=T"
    else:
        ahft_param = ""

    subchart = "&subChart1=3&ref1para1=12&ref1para2=26&ref1para3=9" + "&subChart2=7&ref2para1=16&ref2para2=8&ref2para3=8" +                     "&subChart3=2&ref3para1=16&ref3para2=0&ref3para3=0" + "&subChart4=2&ref4para1=3&ref4para2=0&ref4para3=0"
    scheme = "&scheme=1&com=100&chartwidth=1073&chartheight=950&stockid=" + code
    period = 6
    
    if isinstance(timeframe, TimeFrame):
        period = timeframe.value
    else:
        url = "https://pbs.twimg.com/profile_images/2625053759/4y6hrlmvpijrurd5z51l_400x400.png"
        return url

    print("Code to Quote: [" + code + "]")
    print("Period to Quote: [" + str(period) + "]")    
        
    url = main + indicator + subchart + scheme + "&period=" + str(period) + ahft_param
    
    print("URL: [" + url + "]")  
    
    return url


def get_aastocks_alpha_code(code):

    for x in FxCode:
        if (x.name == code.upper()):
            return str(x.value)
    
    for x in IndexCode:
        if (x.name == code.upper()):
            return str(x.value)
            
    return code.upper() + ".US"
    
def main():

    tf = "h"
    print(get_hkg_chart_list_by_type("MHSIF", tf, []))
    #print(get_hkg_chart_list_by_type("939", tf, ["night"]))
    #print(get_hkg_chart_list_by_type("939", tf, ["3988", "2388", "BABA"]))
    #print(get_hkg_chart_list_by_type("939", tf, ["HSIFN", "2388", "BABA", "bb", "night"]))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



