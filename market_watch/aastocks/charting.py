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
from market_watch.finviz import charting as finviz_charting
from market_watch.yahoo import charting as yahoo_charting

def get_hkg_chart_list_by_type(code, action, params):
    
    url_dict_list = []
    ind_params = []
    ATTRS = ("bb", "sma", "night", "gcc", "line")
    
    for p in params:
        pl = p.lower()
        if pl in ATTRS:
            ind_params.append(pl)

    url_dict_list.append({'code': code, 'url': get_hkg_chart_by_type(code, action, ind_params)})
    
    for p in params:
        if not p in ATTRS:
            url_dict_list.append({'code': p, 'url': get_hkg_chart_by_type(p, action, ind_params)})
    
    return url_dict_list

def get_hkg_chart_list_by_action(action, params):
    
    url_dict_list = []
    ind_params = []
    ATTRS = ("bb", "sma", "night", "gcc", "line")
    
    for p in params:
        pl = p.lower()
        if pl in ATTRS:
            ind_params.append(pl)

    for p in params:
        if not p in ATTRS:
            url_dict_list.append({'code': p, 'url': get_hkg_chart_by_type(p, action, ind_params)})
    
    return url_dict_list   

def get_hkg_chart_by_type_list(code, params):

    url_list = []

    for tf in ("M", "w", "d", "h"):
        url_list.append(get_hkg_chart_by_type(code, tf, params))

    return url_list        

def get_hkg_chart_by_type(code, action, params):

    url = ""
    is_bb = False
    is_ema = False
    is_sma = False
    is_night = False
    is_ahft = False
    is_gcc = False
    is_num = False
    is_CN = False
    is_US = False
    is_FX = False
    is_line = False   
 
    for p in params:
        if (p.lower() == "bb"):
            is_bb = True
        elif (p.lower() == "sma"):
            is_sma = True
        elif (p.lower() == "night"):
            is_night = True
        elif (p.lower() == "gcc"):
            is_gcc = True
        elif (p.lower() == "line"):
            is_line = True
    
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
    elif (finviz_charting.is_finviz_code(code)):
        return finviz_charting.get_finviz_chart(code, action)
    elif (yahoo_charting.is_tse_code(code)):
        return yahoo_charting.get_tse_chart(code, action)    
    elif (code.isalpha()):

        #if ("USD" == code.upper()):
        #    return get_finvinz_chart(code, action)

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
    
    #indicator = "&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
    indicator= "&Indicator=3&indpara1=10&indpara2=20&indpara3=50&indpara4=100&indpara5=200"
    ahft_param = ""    
    chart_type = "1" # candle-stick

    if (is_bb):
        indicator = "&Indicator=9&indpara1=20&indpara2=2&indpara3=0&indpara4=0&indpara5=0"
    if (is_sma):
        indicator = "&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
    if (is_gcc):
        indicator = "&Indicator=1&indpara1=50&indpara2=200"
    if (is_ahft):
        ahft_param = "&AHFT=T"
    if (is_line):
        chart_type = "5" # line
        indicator = "&Indicator=1&indpara1=0"

    main = "https://charts.aastocks.com/servlet/Charts?"
    main = main + "fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&chart=left&type=" + chart_type
 
    subchart = ("&subChart1=3&ref1para1=12&ref1para2=26&ref1para3=9" 
                + "&subChart2=7&ref2para1=16&ref2para2=8&ref2para3=8" 
                + "&subChart3=2&ref3para1=16&ref3para2=0&ref3para3=0" 
                + "&subChart4=2&ref4para1=3&ref4para2=0&ref4para3=0")
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
    #print(get_hkg_chart_list_by_type("4911j", "m", []))
    #print(get_hkg_chart_list_by_type("4911J", "h", []))
    #print(get_hkg_chart_list_by_type("49111", "m", []))
    #print(get_hkg_chart_list_by_type("4922k", "m", []))
    #print(get_hkg_chart_list_by_type("4933J", "M", []))
    #print(get_hkg_chart_list_by_type("MHSIF", tf, []))
    #print(get_hkg_chart_list_by_type("NIKKEI", tf, []))
    #print(get_hkg_chart_list_by_type("BTC", tf, []))
    #print(get_hkg_chart_list_by_type("939", tf, ["night"]))
    #print(get_hkg_chart_list_by_type("939", tf, ["3988", "2388", "BABA"]))
    print(get_hkg_chart_by_type("939", tf, ["line"]))
    print(get_hkg_chart_by_type("MHSIF", tf, ["line", "night"]))
    print(get_hkg_chart_by_type("939", tf, ["gcc", "night"]))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



