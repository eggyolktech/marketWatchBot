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

from enum import Enum

class Timeframe(Enum):
    WEEKLY = 1
    DAILY = 2
    HOURLY = 3
    MINUTE = 4


def get_hkg_chart_by_type(code, timeframe):

    url = ""

    if (timeframe == Timeframe.WEEKLY):    
        url = "http://charts.aastocks.com/servlet/Charts?fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52&subChart1=2&ref1para1=3&ref1para2=0&ref1para3=0&subChart2=2&ref2para1=19&ref2para2=0&ref2para3=0&subChart3=3&ref3para1=12&ref3para2=26&ref3para3=9&subChart4=7&ref4para1=16&ref4para2=5&ref4para3=0&subChart5=7&ref5para1=7&ref5para2=10&ref5para3=0&scheme=1&com=100&chartwidth=1073&chartheight=950&stockid=110000.HK&chart=left&period=11&type=1&&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
        
    elif (timeframe == Timeframe.DAILY):
        url = "http://charts.aastocks.com/servlet/Charts?fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52&subChart1=2&ref1para1=3&ref1para2=0&ref1para3=0&subChart2=2&ref2para1=19&ref2para2=0&ref2para3=0&subChart3=3&ref3para1=12&ref3para2=26&ref3para3=9&subChart4=7&ref4para1=16&ref4para2=5&ref4para3=0&subChart5=7&ref5para1=7&ref5para2=10&ref5para3=0&scheme=1&com=100&chartwidth=1073&chartheight=950&stockid=110000.HK&chart=right&period=6&type=1&&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
    
    elif (timeframe == Timeframe.HOURLY):
        url = "http://charts.aastocks.com/servlet/Charts?fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52&subChart1=2&ref1para1=3&ref1para2=0&ref1para3=0&subChart2=2&ref2para1=19&ref2para2=0&ref2para3=0&subChart3=3&ref3para1=12&ref3para2=26&ref3para3=9&subChart4=7&ref4para1=16&ref4para2=5&ref4para3=0&subChart5=7&ref5para1=7&ref5para2=10&ref5para3=0&scheme=1&com=100&chartwidth=1073&chartheight=950&stockid=110000.HK&chart=left&period=5023&type=1&&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
 
    elif (timeframe == Timeframe.MINUTE):
        url = "http://charts.aastocks.com/servlet/Charts?fontsize=12&15MinDelay=F&lang=1&titlestyle=1&vol=1&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52&subChart1=2&ref1para1=3&ref1para2=0&ref1para3=0&subChart2=2&ref2para1=19&ref2para2=0&ref2para3=0&subChart3=3&ref3para1=12&ref3para2=26&ref3para3=9&subChart4=7&ref4para1=16&ref4para2=5&ref4para3=0&subChart5=7&ref5para1=7&ref5para2=10&ref5para3=0&scheme=1&com=100&chartwidth=1073&chartheight=950&stockid=110000.HK&chart=left&period=5023&type=1&&Indicator=1&indpara1=4&indpara2=6&indpara3=14&indpara4=27&indpara5=40&indpara6=52"
     
    else:
        url = "https://pbs.twimg.com/profile_images/2625053759/4y6hrlmvpijrurd5z51l_400x400.png"

    return url

              
def main():

    print(get_hkg_chart_by_type("TEST", Timeframe.MINUTE))
    
if __name__ == "__main__":
    main()                
              



