#!/usr/bin/python


from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

def get_profile(code):

    DEL = "\n\n"
    EL = "\n"
    CL = ":"
    URL = "http://www.aastocks.com"

    if (is_number(code)):
        print("Code to Quote: [" + code + "]")
    else:
        return "<i>Usage:</i> " + "/qS" + "[StockCode] (e.g. " + "/qS2899" + ")"   
    url = "http://www.aastocks.com/tc/stocks/analysis/company-fundamental/company-information?symbol=%s" % (code)
     
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    
    passage = ""
    count = 0

    tableCorp = soup.find('table', {'class', 'cnhk-cf'})
    
    if (tableCorp):
    
        trows = tableCorp.findAll("tr", recursive=False)
        
        if (len(trows[0].findAll('td')) < 2):
            return "Information Not Available"
        
        major_holders = trows[0].findAll('td')[1].text.strip()

        if (major_holders):
            #passage = "<b>(" + code + ")</b>" + DEL
            
            for row in trows:

                tag = row.findAll('td')[0].text
                desc = row.findAll('td')[1]
                while (desc.find('br')):
                    desc.find('br').replaceWith(EL)
                
                desc = desc.text
                #print(desc)
                if (tag == "相關上市公司"):
                    continue

                passage = passage + tag  + CL + EL
                passage = passage + desc + DEL
        else:
            return "Information Not Available"
    else:
        return "Information Not Available"

    url = "http://www.aastocks.com/tc/stocks/analysis/company-fundamental/company-profile?symbol=%s" % (code)
     
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    
    tableCorp = soup.find('table', {'class', 'cnhk-cf'})
    
    if (tableCorp):
    
        trows = tableCorp.findAll("tr", recursive=False)
        
        if (len(trows[0].findAll('td')) > 1):
        
            major_holders = trows[0].findAll('td')[1].text.strip()

            if (major_holders):
                #passage = "<b>(" + code + ")</b>" + DEL
            
                for row in trows:

                    tag = row.findAll('td')[0].text
                    desc = row.findAll('td')[1]
                    while (desc.find('br')):
                        desc.find('br').replaceWith(EL)
                
                    desc = desc.text
                    passage = passage + tag  + CL + EL
                    passage = passage + desc + DEL

    if (not passage):
        passage = "No profile!"
    else:
        passage = "<i>Company Profile for " + code + ".HK</i>" + DEL + passage
    
    return passage   
    
def main():

    print(get_profile("7200"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
     
if __name__ == "__main__":
    main()                
              



