#!/usr/bin/python

import pandas as pd
import pandas_datareader.data as web  # Package and modules for importing data; this code may change depending on pandas version
import time
import datetime
import json

import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import matplotlib.pyplot as plt   # Import matplotlib

from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import csv

import traceback
import logging

from market_watch.common.AastocksConstants import *

def get_stocks_rs_industry_list():

    passage = "List Relative Strength by Industries" + DEL + "/qRHK (HSI Indexes)" + EL
    passage = passage + "/qRUS1 (US ETF by Sectors)" + EL
    passage = passage + "/qRUS2 (US Major ETF)" + EL

    with open('../data/list_TopIndustryList.json', encoding="utf-8") as data_file:    
        indexlists = json.load(data_file)    
        
    for indexlist in indexlists:
        code = indexlist["code"]
        passage = passage + "/qR" + code + " (" + indexlist["label"] + ")" + EL  
    
    return passage  
    
def get_stocks_rs_list(code, limit):

    result = []
    codelist = []
    
    if (code.upper() == "HK"):

        INDEX_LIST = [('HSI', 'INDEXHANGSENG:HSI'), ('HSCEI', 'INDEXHANGSENG:HSCEI'), ('HSP', 'INDEXHANGSENG:HSI.P'), ('HSF', 'INDEXHANGSENG:HSI.F'), ('HSU', 'INDEXHANGSENG:HSI.U'), ('HSC', 'INDEXHANGSENG:HSI.C')]
        
        passage = "HK Sector List: " + DEL
        
        for key, value in INDEX_LIST:
            codelist.append(value)
            passage = passage + key + " (" + value + ")" + EL

    elif ("US" in code.upper()):
    
        if (code.upper()[-1] == "1"):
            INDEX_LIST = [('Technology SPRD', 'XLK'), ('Financial SPRD', 'XLF'), ('Energy SPRD', 'XLE'), ('Industrial SPRD', 'XLI'), ('Utilities SPRD', 'XLU'), ('Health Care SPRD', 'XLV'), ('Consumer Staples SPRD', 'XLP'), ('Consumer Discretionary SPRD', 'XLY'), ('Materials SPRD', 'XLB'), ('Gold SPRD', 'GLD'), ('S&P', 'INDEXCBOE:SPX') ]
        else:
            INDEX_LIST = [('Vanguard Developed Market', 'VEA'), ('Vanguard Emerging Market', 'VWO'),  ('Vanguard REIT', 'VNQ'), ('Gold SPRD', 'GLD'), ('20Y TBond', 'TLT'), ('S&P', 'INDEXCBOE:SPX') ]
        
        passage = "US Sector List: " + DEL
        
        for key, value in INDEX_LIST:
            codelist.append(value)
            passage = passage + key + " (" + value + ")" + EL            
            
    else:
    
        with open('../data/list_TopIndustryList.json', encoding="utf-8") as data_file:    
            indexlists = json.load(data_file)  
        
        filtered_index = [x for x in indexlists if x['code'] == code]
        
        passage = "Top " + str(limit) + " Stocks List in " + filtered_index[0]['label'] + "" + DEL
        
        if (filtered_index):
            for stock in filtered_index[0]["list"][0:limit]:
                codelist.append(stock["code"])
                passage = passage + stock["code"] + " (" + stock["label"] + ")" + EL
        else:
            passage = u'\U000026D4' + ' List Not Available'
        
    result.append(passage)
    result.append(codelist)
    return result

def get_historical_price_from_google(code):

    print("Retrieved Data from Google for code: [" + code + "]")
    url1 = 'http://www.google.com.hk/finance/historical?q=' + code + '&num=200&start=0'
    url2 = 'http://www.google.com.hk/finance/historical?q=' + code + '&num=200&start=200'
    r1 = urllib.request.urlopen(url1)
    r2 = urllib.request.urlopen(url2)
    soup = BeautifulSoup(r1, "html5lib")
    tabulka = soup.find("table", {"class" : "gf-table historical_price"})

    soup = BeautifulSoup(r2, "html5lib")
    tabulkb = soup.find("table", {"class" : "gf-table historical_price"})
    
    if not os.name == 'nt':
        csvfilename = "/tmp/histdata/" + code.replace(":", "") + '.csv'
    else:    
        csvfilename = "C:\\Temp\\histdata\\" + code.replace(":", "") + '.csv'

    with open(csvfilename, 'w') as csvfile:

        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in tabulka.findAll('tr')[1:]:
            col = row.findAll('td')
            date = col[0].string.strip()
            sopen = col[1].string.replace(",", "").strip()
            high = col[2].string.replace(",", "").strip()
            low = col[3].string.replace(",", "").strip()
            close = col[4].string.replace(",", "").strip()
            volume = col[5].string.replace(",", "").strip()
            
            #print(",".join([date, sopen, high, low, close, volume]))
            writer.writerow({'Date': date, 'Open': sopen, 'High': high, 'Low': low, 'Close': close, 'Volume': volume})

        if (tabulkb and len(tabulkb.findAll('tr')) > 0):
            for row in tabulkb.findAll('tr')[1:]:
                col = row.findAll('td')
                date = col[0].string.strip()
                sopen = col[1].string.replace(",", "").strip()
                high = col[2].string.replace(",", "").strip()
                low = col[3].string.replace(",", "").strip()
                close = col[4].string.replace(",", "").strip()
                volume = col[5].string.replace(",", "").strip()
                
                #print(",".join([date, sopen, high, low, close, volume]))
                writer.writerow({'Date': date, 'Open': sopen, 'High': high, 'Low': low, 'Close': close, 'Volume': volume})        

    df = pd.DataFrame.from_csv(csvfilename, header=0, sep=',', index_col=0)
    df.sort_index(inplace=True)
    
    #print(df.head())    
    return df
    
def get_stocks_rs_charts(codelist):

    DEL = "\n\n"
    EL = "\n"
    chartpath = ""
    codelist = codelist[:15]
     
    # We will look at stock prices over the past year, starting at April 1, 2016
    now = datetime.datetime.now()
    start = datetime.datetime(2016, now.month, 1)
    end = datetime.date.today()

    #for code in codelist:
    #    if (not is_number(code)):
    #        raise ValueError("Non-numeric code found: [" + code + "]\n<i>Usage:</i> " + "/qr" + "[code1] [code2] [code3].... (e.g. " + "/qr2800 2822 2823" + ")")    

    startdatelist = []  
    stockcodelist = []
    codedflist = []
    invalidcodelist = []
    result = []    
    
    INDEX_LIST = [('HSI', 'INDEXHANGSENG:HSI'), ('HSCEI', 'INDEXHANGSENG:HSCEI'), ('HSP', 'INDEXHANGSENG:HSI.P'), ('HSF', 'INDEXHANGSENG:HSI.F'), ('HSU', 'INDEXHANGSENG:HSI.U'), ('HSC', 'INDEXHANGSENG:HSI.C'), ('DAX', 'INDEXDB:DAX'), ('SPX', 'INDEXCBOE:SPX'), ('NASDAQ', 'INDEXNASDAQ:NDX'), ('DJI', 'INDEXDJX:.DJI'), ('NIKKEI', 'INDEXNIKKEI:NI225'), ('FTSE', 'INDEXFTSE:UKX'), ('CAC', 'INDEXEURO:PX1'),('Vanguard Developed Market', 'VEA'), ('Vanguard Emerging Market', 'VWO'),  ('Vanguard REIT', 'VNQ'), ('Technology SPRD', 'XLK'), ('Financial SPRD', 'XLF'), ('Energy SPRD', 'XLE'), ('Industrial SPRD', 'XLI'), ('Utilities SPRD', 'XLU'), ('Health Care SPRD', 'XLV'), ('Consumer Staples SPRD', 'XLP'), ('Consumer Discretionary SPRD', 'XLY'), ('Materials SPRD', 'XLB'), ('Gold SPRD', 'GLD'), ('20Y TBond', 'TLT'), ('S&P', 'INDEXCBOE:SPX'), ('SHA', 'SHA:000001') ]
            
    for code in codelist:
        
        if (code[0] == "0"):
            code = code[1:]
        
        if (is_number(code)):
            code = "HKG:" + code.rjust(4, '0')
        else:
            code = code.upper()
            
            for key, value in INDEX_LIST:
                if (code == key):
                    code = value
                    break
        
        try:
            #codedf = web.DataReader(code, "yahoo", start, end)            
            codedf = get_historical_price_from_google(code)
            
            stockcodelist.append(code)
            codedflist.append(codedf)
            startdatelist.append(codedf.index[0])

        except Exception as e:
            logging.error(" Error getting code: " + code)
            logging.error(traceback.format_exc())
            invalidcodelist.append(code)   
        
    maxstartdate = max(startdatelist)   
    codedfloclist = []
    
    for codedf in codedflist:
        codedf = codedf.loc[maxstartdate:]
        codedfloclist.append(codedf)    
    
    # form the df dict
    codedic = {}
    
    for idx, codeval in enumerate(stockcodelist):
        codedic[codeval] = codedfloclist[idx]["Close"]
    
    stocks = pd.DataFrame(codedic)
    
    stocks_return = stocks.apply(lambda x: x / x[0])    
    stocks_return_6_months = stocks.tail(23*6).apply(lambda x: x / x[0])
    stocks_return_3_months = stocks.tail(23*3).apply(lambda x: x / x[0])
    stocks_return_1_month = stocks.tail(23).apply(lambda x: x / x[0])

    #print(stocks_return.tail())
    
    #plt.style.use('seaborn-white')
    #plt.style.use('dark_background')
    plt.style.use('bmh')
    #plt.style.use('ggplot')
    #plt.style.use('fivethirtyeight')
    
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Ubuntu Mono'
    plt.rcParams['font.size'] = 8

    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 9
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['legend.fontsize'] = 8
    plt.rcParams['figure.facecolor'] = '#fffff9'
    plt.rcParams['figure.titlesize'] = 8
    
    fig = plt.figure(figsize=(10,6))
    
    ax1 = fig.add_subplot(221)
    ax1.xaxis.label.set_visible(False)
    ax1.set_title("RS (1 Month)")
    stocks_return_1_month.plot(ax=ax1)
    
    ax2 = fig.add_subplot(222)
    ax2.xaxis.label.set_visible(False)
    ax2.set_title("RS (3 Months)")
    stocks_return_3_months.plot(ax=ax2)

    ax3 = fig.add_subplot(223)
    ax3.xaxis.label.set_visible(False)
    ax3.set_title("RS (6 Months)")
    stocks_return_6_months.plot(ax=ax3)

    ax4 = fig.add_subplot(224)
    ax4.xaxis.label.set_visible(False)
    ax4.set_title("RS (1 Year)")
    stocks_return.plot(ax=ax4)    
    
    #ax3 = fig.add_subplot(212)
    #stocks_return.plot(ax=ax3)
    
    #stocks_return.plot(figsize=(10,6), grid = True, linewidth=1.0, title="Relative Strength since 2016", colormap = plt.cm.Dark2).axhline(y = 1, color = "black", lw = 1) 
    #plt.legend(loc='upper left')
    #stocks.plot()
    
    if not os.name == 'nt':
        chartpath = "/tmp/rscharts/" + 'gchart' + str(int(round(time.time() * 1000))) + '.png'
    else:
        chartpath = "C:\\Temp\\rscharts\\" + 'gchart' + str(int(round(time.time() * 1000))) + '.png'
    
    #print(chartpath)
    
    plt.tight_layout()
    plt.savefig(chartpath, bbox_inches='tight')
    plt.show()
    
    result.append(chartpath)
    result.append(invalidcodelist)
    return result
    
   
def main():

    try:
        #print(get_stocks_rs_charts("494 293".split()))
        #print(get_stocks_rs_charts("2388111 5 11".split()))
        
        #print(get_stocks_rs_charts("HSI HSCEI HSP HSF HSU HSC".split())) 
        #print(get_stocks_rs_charts("HSI 700 941 3988".split())) 
        print(get_stocks_rs_charts("HSI 700".split()))
        #print(get_stocks_rs_charts("2388".split()))
        #print(get_stocks_rs_charts("66 2388".split()))
        #print(get_stocks_rs_charts(["66", "2828", "2800"]))
        #print(get_stocks_rs_charts("1357 799 700 BABA FB MSFT AAPL".split()))
    except ValueError as ve:
        print("Value Error: [" + str(ve) + "]")
        logging.error(traceback.format_exc())
    except Exception as e:
        print("Exception: [" + str(e) + "]")
        logging.error(traceback.format_exc())
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



