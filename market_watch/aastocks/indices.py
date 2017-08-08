#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime



def get_indices(region):

    DEL = "\n\n"
    EL = "\n"

    url = "http://www.aastocks.com/tc/mobile/Indices.aspx"
    
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    indicesTable = soup.findAll("table", {"class": "quote_table_header"})

    indices = indicesTable[0]
    if (region == "hk"):
        indices = indicesTable[0]
    elif (region == "cn"):
        indices = indicesTable[1]
    elif (region == "w"):
        indices = indicesTable[2]
    
    passage = "<b>" + indices.findAll("tr")[0].findAll("td")[0].text + "</b>" + DEL

    for tr in indices.findAll("tr")[1:-1]:

        name = tr.findAll("td")[0].text
        last = tr.findAll("td")[1].text
        change = tr.findAll("td")[2].text  
        change = change.replace("+", u'\U0001F53A').replace("-", u'\U0001F53B')

        passage = passage + name + ": " + last + " " + change + "" + EL
   
    passage = passage + EL + "<i>" +  indices.findAll("tr")[-1].findAll("td")[0].text + "</i>"
 
    if (not passage):
        passage = "No indices found."
    
    return passage   
    
def main():

    print(get_indices("hk"))
    print(get_indices("cn"))
    print(get_indices("w"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



