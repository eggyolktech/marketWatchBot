#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import re
import os
from datetime import date
from datetime import datetime
from selenium import webdriver


def get_shareholding_disclosure(code):

    DEL = "\n\n"
    EL = "\n"
    passage = ""

    if (is_number(code)):
        print("Code to Quote: [" + code + "]")           
    else:
        return "<i>Usage:</i> " + "/qC" + "[StockCode] (e.g. " + "/qC2899" + ")"   
        
    url = "http://sdinotice.hkex.com.hk/filing/di/NSSrchCorpList.aspx?sa1=cl&scsd=01/01/2017&sced=06/05/2017&sc=" + code + "&src=MAIN&lang=ZH"

    print("Url: [" + url + "]")
    
    r = requests.get(url)
    html = r.text
    
    soup = BeautifulSoup(html, "html.parser")
    
    masterTable = soup.find('table', id="grdPaging")
    
    # record found
    if (len(masterTable.findAll('tr')) > 1):
        name = masterTable.findAll('tr')[1].findAll('td')[1].text.strip()
        link = masterTable.findAll('tr')[1].findAll('td')[2].findAll('a')[1]['href']
        
        # detail table
        print("Detail Url: [" + 'http://sdinotice.hkex.com.hk/filing/di/' + link + "]")
        r2 = requests.get('http://sdinotice.hkex.com.hk/filing/di/' + link)
        print(r2.headers['content-type'])
        html2 = r2.text
        
        soup2 = BeautifulSoup(html2, "html.parser")
        
        detailTable = soup2.find('table', id="grdPaging")
        
        # record found
        if (len(detailTable.findAll('tr')) > 1):
        
            passage = "<i>Substantial Shareholders for " + code + " (" + name + ")</i>" + DEL
            passage = passage + "*Notes: (L) - Long Position, (S) - Short Position, (P) - Lending Pool" + DEL
            
            for tr in detailTable.findAll('tr')[1:]:
                cols = tr.findAll('td')
                passage = passage + "<b>" + cols[0].text + "</b>" + EL
                passage = passage + "Holder: " + ", ".join(cols[1].strings) + EL
                passage = passage + "Shares: " + (", ".join(cols[2].strings)) + EL + "% of Capital: " + cols[3].text.replace("(","%(") + DEL
   
    if (not passage):
        passage =  u'\U000026D4' + (" %s 沒有股權披露" % code)

    return passage
        
def get_latest_ccass_info(code, number, is_simple=False):

    DEL = "\n\n"
    EL = "\n"
    passage = ""
   
    #return "Job failed, please go to <a href='http://www.hkexnews.hk/sdw/search/searchsdw_c.aspx'>here</a> directly"
 
    if (os.name == 'nt'):
        browser = webdriver.Chrome('C:\project\common\chromedriver.exe')
    else:
        browser = webdriver.PhantomJS() 
 
    if (is_number(code) and is_number(number)):
        print("Code to Quote: [" + code + "]")
        print("Number to Grab: [" + str(number) + "]")           
    else:
        return "<i>Usage:</i> " + "/qC" + "[StockCode] (e.g. " + "/qC2899" + ")"   
    
    browser.get(r'http://www.hkexnews.hk/sdw/search/searchsdw_c.aspx')

    elemCode = browser.find_element_by_name('txtStockCode')
    elemCode.send_keys(code)
    
    elemSearch = browser.find_element_by_id('btnSearch')
    elemSearch.click()
    
    # Detect if there is any alert
    try:
        alert = browser.switch_to_alert()
        error = alert.text
        alert.accept()
        print("alert accepted")
        browser.close()
        return  u'\U000026D4' + " " + error
    except:
        print("no alert")
    
    html = browser.page_source
    
    browser.close()

    #print("Result: [" + str(html.encode("utf-8")) + "]")  
    
    soup = BeautifulSoup(html, "html.parser")
    masterDiv = soup.find('div', id="pnlResultSummary")
   
    if not (masterDiv):
        return u'\U000026D4' + " " +  ('股票號碼 %s 不存在或不設查詢' % code)
 
    totalDiv = masterDiv.find('div', {'class': 'ccass-search-total'})
    
    div = soup.find('div', id="pnlResultNormal")    
    title = ""
    simple_result = []
    
    # Stock code exists
    if (div):
    
        # get total participants info first
        num_intermediates = totalDiv.find('div', {'class': 'number-of-participants'}).find('div', {'class': 'value'}).text.strip()
        shares_percentage = totalDiv.find('div', {'class': 'shareholding'}).find('div', {'class': 'value'}).text.strip()
        
        passage = "Number of Participants: " + num_intermediates + " (Shares: " + shares_percentage + ")"
        simple_result.append(num_intermediates)
        simple_result.append(shares_percentage)

        passage = passage + DEL
       
        title = "%s (%s)" % (soup.find('input', {'name': 'txtStockName'}).get('value'), code) 
        ctable = soup.find('table', {'class': 'table-mobile-list'})  
        rows = ctable.findAll('tr')[1:1+number]
        count = 1
            
        for row in rows:
            cols = row.findAll('div', {'class': 'mobile-list-body'})
              
            pid = cols[0].text.strip("/r/n").strip()
            pname = cols[1].text.strip("/r/n").strip()
            pshares = cols[3].text.strip("/r/n").strip()
            ppercentage = cols[4].text.strip("/r/n").strip()

            simple_result.append([pid, pname, pshares, ppercentage])
            
            #passage = passage + str(count) + ": " + pid + " - " + pname + " (" + pshares + ", " + ppercentage + ")" + EL
            passage = passage + str(count) + ". " + pname + "" + EL + "Shares: " + pshares + " (" + ppercentage + ")" + DEL           
            count = count + 1
    
    if (is_simple):
        return simple_result

    if (not passage):
        passage =  u'\U000026D4' + " " +  ('股票號碼 %s 不存在或不設查詢' % code)
    else:
        passage = "<i>Top CCASS for " + title + "</i>" + DEL + passage
    
    return passage   
    
def main():

    print(get_latest_ccass_info("2630", 5))
 
    #print(get_latest_ccass_info("939", 5, True))
   
    #print(get_latest_ccass_info("99999", 5).encode("utf-8"))
    
    #print(get_shareholding_disclosure("1980").encode("utf-8"))
    #print(get_shareholding_disclosure("1810").encode("utf-8"))

    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



