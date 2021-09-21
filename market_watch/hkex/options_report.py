#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime, timedelta
from market_watch.telegram import bot_sender
import pandas as pd
import os
import time
from bs4 import BeautifulSoup
from market_watch.util import chart_helper

EL = "\n"
DEL = "\n\n"

def get():

    if (datetime.now().hour > 20):
        cdate = datetime.strftime(datetime.now(), "%y%m%d")
    else:
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        cdate = datetime.strftime(yesterday, "%y%m%d")
   
    print(cdate)
    url = 'https://www.hkex.com.hk/chi/stat/dmstat/dayrpt/dqec%s.htm' % cdate
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    summary = soup.find("a", {'name': 'SUMMARY'})

    sor = False
    datasets = []

    for line in summary.text.splitlines():
    
        line = line.encode('ISO-8859-1').decode('big5', errors='ignore')    
        if len(line) > 0 and sor:    
            opx = line.split()
            if '$' in opx[2]:
                dataset = (opx[3][1:-1], opx[1], opx[4], opx[5], opx[6], opx[-1])
            else:
                dataset = (opx[2][1:-1], opx[1], opx[3], opx[4], opx[5], opx[-1])
                print(dataset)
                datasets.append(dataset)
        elif sor:
            break
    
        if "代號" in line:
            sor = True
    
    #print(datasets)
    cols = ['Code', 'Stock', 'VolTotal', 'VolCalls', 'VolPuts', 'IV']
    df = pd.DataFrame.from_records(datasets, index='Code', columns=cols)
    df = df.sort_values(by=['IV'])

    return df 

def gen_opx_report():

    try:
        df = get()
    except:
        return None   
    
    print(df)
    return chart_helper.get_table_chart(df, "opxreport")

def main():

    print(gen_opx_report())

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              
