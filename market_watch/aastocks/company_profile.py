#!/usr/bin/python


from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import ast

DEL = "\n\n"
EL = "\n"
CL = ":"
URL = "http://www.aastocks.com"

def get_dividend(code):

    if (is_number(code)):
        print("Code to Quote: [" + code + "]")
    else:
        return "<i>Usage:</i> " + "/qp" + "[StockCode] (e.g. " + "/qp1660" + ")"   
    url = "https://www.etnet.com.hk/www/eng/stocks/realtime/quote_dividend.php?code=%s" % (code)
     
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    passage = ""
    
    div = soup.find("div", {"class": "DivFigureContent"})

    if (div and div.find("script")):
        t = (div.find("script").text.strip().replace("drawComboChart", "").replace(";",""))
        t = ast.literal_eval(t)
        dates = [date.replace("\\","").strip() for date in t[2]]
        dpsl = [dps for dps in t[3]]
        ratios = [ratio for ratio in t[4]]
    else:
        return ("No dividend history for [%s]" % code)

    for idx, val in enumerate(dates):

        passage = passage + ("%s: $%.3f (%s%%)" % (val, dpsl[idx], ratios[idx])) + EL
    
    if (not passage):
        return ("No dividend history for [%s]" % code)
    else:
        passage = "<i>Dividend History for " + code + ".HK</i>" + DEL + passage
    
    return passage   
 
def get_ocf(code):

    if (is_number(code)):
        print("Code to Quote: [" + code + "]")
    else:
        return "<i>Usage:</i> " + "/qp" + "[StockCode] (e.g. " + "/qp1660" + ")"   
    url = "http://aastocks.com/tc/stocks/analysis/company-fundamental/cash-flow?symbol=%s" % (code)
     
    print("URL: [" + url + "]")  
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    passage = ""
    count = 0
    table = soup.find('table', {'class', 'cnhk-cf'})
    
    try:
        cols = table.findAll('tr')[0].findAll("td")[1:-1]
        dates = []
        for col in cols:
            if col.text.strip() != "":
                dates.append(col.text.strip())

        cols = table.findAll('tr')[1].findAll("td")[1:-1]
        ocfs = []
        for col in cols:
            if col.text.strip() != "":
                ocfs.append(col.text.replace(',','').strip())

    except:
        print("Exception found!")
        return ("No ocf history for [%s]" % code)

    #print(dates)
    #print(ocfs)

    for idx, val in enumerate(dates):

        if idx > 0:
            print("%s / %s" % (ocfs[idx], ocfs[idx-1]))
            change_pct = (int(ocfs[idx]) - int(ocfs[idx-1])) / int(ocfs[idx-1])
            if change_pct > 0:
                change_pct = u'\U0001F332' + ("%.2f" % (change_pct*100))
            elif change_pct < 0:
                change_pct = u'\U0001F53B' + ("%.2f" % (change_pct*100)).replace("-","")
        else:
            change_pct = "-"
        
        passage = passage + ("%s: %s (%s%%)" % (val, ocfs[idx].replace("-", u'\U00002796'), change_pct)) + EL

    if (not passage):
        return ("No ocf history for [%s]" % code)
    else:
        passage = "<i>Net Operating Cashflow for " + code + ".HK</i>" + DEL + passage
    
    return passage   
 

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

    for code in ["1233", "700", "1660", "87001"]:
        print(get_ocf(code))
        #print(get_dividend(code))

    #print(get_ocf("1660"))
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
     
if __name__ == "__main__":
    main()                
              



