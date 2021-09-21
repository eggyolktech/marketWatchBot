#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
from market_watch.telegram import bot_sender
import pandas as pd
import os
import matplotlib as mpl
import time

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import matplotlib.pyplot as plt



EL = "\n"
DEL = "\n\n"

def get():

    url = "https://finance.yahoo.com/calendar/earnings"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=20)
    html = r.text 
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
   
    title = soup.find("div", {'id': 'fin-cal-table'}).find("h3").find("span").text.strip()

    passage = "<b>" + title + "</b>" + DEL
    rows = soup.find("div", {'id': 'cal-res-table'}).find('tbody').find_all('tr')

    for row in rows[:30]:
        cols = row.findAll("td")
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        earncalltime = cols[2].text.strip()
        eps_est = cols[3].text.strip()

        passage = passage + ("/qv%s - %s (%s)" % (symbol, name, earncalltime)) + EL
 
    return passage 

def get_stock(code):

    url = "https://finance.yahoo.com/calendar/earnings/?symbol=%s" % code.upper()

    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers, timeout=20)
    html = r.text 
    #print(html)
    soup = BeautifulSoup(html, "html.parser")
   
    #title = soup.find("div", {'id': 'fin-cal-table'}).find("h3").find("span").text.strip()

    passage = "<b>Earning History (%s)" % code.upper()+ "</b>" + DEL

    rows = soup.find("div", {'id': 'cal-res-table'}).find('tbody').find_all('tr')

    earndate_list = []
    eps_est_list = []
    eps_act_list = []
    suprise_list = []

    for row in rows[:20]:
        cols = row.findAll("td")
        symbol = cols[0].text.strip()
        name = cols[1].text.strip()
        print(cols[2].text.strip())
        earndate_list.append(cols[2].text.strip())
        eps_est_list.append(cols[3].text.strip())
        eps_act_list.append(cols[4].text.strip())
        suprise_list.append(cols[5].text.strip())
       
    data  = {'Earning Dates': earndate_list,
             'EPS Estimate': eps_est_list,
             'EPS Actual': eps_act_list,
             'Suprise(%)': suprise_list 
            }
    df = pd.DataFrame (data, columns = ['Earning Dates', 'EPS Estimate', 'EPS Actual', 'Suprise(%)'])
       
    return df 

def tablized(df):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    #df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
    #print(df)
    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    if not os.name == 'nt':
        #chartpath = "/tmp/rscharts/" + 'gchartsma' + str(int(round(time.time() * 1000))) + '.png'
        chartpath = "/tmp/rscharts/" + 'yahooearning' + str(int(round(time.time() * 1000))) + '.png'
    else:
        chartpath = "C:\\Temp\\rscharts\\" + 'gchart' + str(int(round(time.time() * 1000))) + '.png'

    print(chartpath)

    plt.tight_layout()
    plt.savefig(chartpath)
    return chartpath

def gen_earning_chart(code):

    try:
        df = get_stock(code)
    except:
        return None   
    
    print(df)
    return tablized(df)

def main():

    print(gen_earning_chart("GOOGL"))
    #bot_sender.broadcast(passage, False)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              
