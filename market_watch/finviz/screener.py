#!/usr/bin/python

from bs4 import BeautifulSoup, Comment
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
import os
from datetime import date
from datetime import datetime
from selenium import webdriver
from market_watch.telegram import bot_sender

def get_screener(url):

    DEL = "\n\n"
    EL = "\n"

    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text 
    soup = BeautifulSoup(html, "html.parser")

    #print(soup)
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    
    lines = None    
    for comment in comments:
        if "TS" in comment and "TE" in comment:
            lines = comment.splitlines()
            lines = lines[1:-1]
            break

    codes = []
    for stkline in lines:
        stks = stkline.split("|")
        codes.append(stks[0])
 
    return codes

def get_screener_urls():

    url = "https://finviz.com/screener.ashx?v=161&f=cap_midover,sh_opt_option,ta_perf_ytd30o,ta_rsi_nos50,ta_sma20_sa50,ta_sma200_pa30,ta_sma50_sa200&ft=3&o=-marketcap"
    urls = [url]
    print("URL: [" + url + "]")

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a", {"class", "screener-pages"})

    for link in links:
        urls.append('https://finviz.com/' + link['href'])

    return urls

def main():
    
    urls = get_screener_urls()
    print(urls)

    codes = []
    for url in urls:    
        stks = get_screener(url)
        codes = codes + stks

    with open("/var/www/eggyolk.tech/html/scripts/fdata.js", "w") as outfile:
        outfile.write("var stockList = ")
        print(codes, file=outfile)
        outfile.write(";")
    #outfile.write("
    print(codes)

    #        bot_sender.send_remote_image(url, "telegram-chat-test")
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



