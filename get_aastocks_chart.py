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

from classes.TimeFrame import TimeFrame

def get_hkg_chart_by_type(code, timeframe):

    url = ""
    
    if (is_number(code)):
        code = code + ".HK"    
    elif (code.isalpha()):
        code = code + ".US"
    else:
        code = "110000.HK"    
    
    main = "http://charts.aastocks.com/servlet/Charts?fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&chart=left&type=1"
    sma = "&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
    subchart = "&subChart1=3&ref1para1=12&ref1para2=26&ref1para3=9" + "&subChart2=7&ref2para1=16&ref2para2=5&ref2para3=0" +                     "&subChart3=2&ref3para1=19&ref3para2=0&ref3para3=0" + "&subChart4=2&ref4para1=3&ref4para2=0&ref4para3=0"
    scheme = "&scheme=1&com=100&chartwidth=1073&chartheight=950&stockid=" + code
    period = 6
    
    if isinstance(timeframe, TimeFrame):
        period = timeframe.value
    else:
        url = "https://pbs.twimg.com/profile_images/2625053759/4y6hrlmvpijrurd5z51l_400x400.png"
        return url

    print("Code to Quote: [" + code + "]")
    print("Period to Quote: [" + str(period) + "]")    
        
    url = main + sma + subchart + scheme + "&period=" + str(period)
    
    print("URL: [" + url + "]")  
    
    return url

              
def main():

    print(get_hkg_chart_by_type("939", TimeFrame.MINUTE))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



