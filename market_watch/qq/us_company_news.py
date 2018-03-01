#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
import os
from datetime import date
from datetime import datetime
from selenium import webdriver

def get_latest_news_by_code(code, number):

    DEL = "\n\n"
    EL = "\n"

    if (not is_number(code) and is_number(number)):
        print("Code to Quote: [" + code + "]")
        print("Number to Grab: [" + str(number) + "]")           
    else:
        return "<i>Usage:</i> " + "/qn" + "[Symbol] (e.g. " + "/qnBABA" + ")"   
    
    url = "http://gu.qq.com/us.%s.N/gg/news" % (code.upper())
    
    print("URL: [" + url + "]")  
    
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    if (os.name == 'nt'):
        browser = webdriver.Chrome('C:\project\common\chromedriver.exe')
    else:
        browser = webdriver.PhantomJS()

    browser.get(url)

   # Detect if there is any alert
    try:
        alert = browser.switch_to_alert()
        error = alert.text
        print("error: " + error)
        alert.accept()
        print("alert accepted")
        browser.close()
    except:
        print("no alert")

    html = browser.page_source

    #r = requests.get(url, headers=headers)
    #html = r.text
    soup = BeautifulSoup(html, "html.parser")
    #print(soup) 
    passage = ""
    count = 0

    divNews = soup.find('div', {"class": "ykbar"}).parent

    #for link in soup.findAll('a', {"class", "market_current_title"}):
    #    aURL = BURL + link['href']
    #    aTitle = link.text

    #    passage = passage + DEL + "<a href='" + aURL + "' target='_blank'>" + aTitle + "</a>" 

    if divNews:

        for link in divNews.findAll('a'):
            aURL = link['href']
            aTitle = link.text
            aUpdate = link.parent.find('span').text
            count = count + 1

            passage = passage + DEL + "<a href='" + aURL + "' target='_blank'>" + aTitle + "</a>"
            passage = passage + " (" + aUpdate + ")"

            if count >= number:
                break
            #print(aURL)

    if (not passage):
        passage = "No news is good news!"
    else:
        passage = "<i>Latest News Feed for " + code + "</i>" + passage
    
    return passage   
    
def main():

    #print(get_latest_news_by_code("JPM", 5).encode("utf-8"))
    print(get_latest_news_by_code("BABA", 10).encode("utf-8"))
    #print(get_latest_news_by_code("XFHG", 5).encode("utf-8"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



