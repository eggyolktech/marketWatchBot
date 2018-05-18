#!/usr/bin/python

from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime

DICT_FINVIZ_FUTURES = {'DJI':['YM', 'Dow Jones Index'], 
                'SPX':['ES', 'S&P 500'],
                'NQ':['NQ', 'Nasdaq 100'],
                'RUSSELL':['ER2', 'Russell 2000'],
                'NIKKEI':['NKD', 'Nikkei 225'],
                'EX':['EX', 'Euro Stoxx 50'],
                'DAX':['DY', 'DAX'],
                'VIX':['VX', 'VIX'],
                'WTI':['CL', 'Crude Oil WTI'],
                'BRENT':['QA', 'Crude Oil Brent'],
                'RBOB':['RB', 'Gasoline RBOB'],
                'HO':['HO', 'Heating Oil'],
                'NGAS':['NG', 'Natural Gas'],
                'ETHANOL':['ZK', 'Ethanol'],
                'GOLD':['GC', 'Gold'],
                'SILVER':['SI', 'Silver'],
                'PLATINUM':['PL', 'Platinum'],
                'COPPER':['HG', 'Copper'],
                'PALLADIUM':['PA', 'Palladium'],
                'OATS':['ZO', 'Oats'],
                'SOYBEANS':['ZS', 'Soybeans'],
                'WHEAT':['ZW', 'Wheat'],
                'COCOA':['CC', 'Cocoa'],
                'COTTON':['CT', 'Cotton'],
                'COFFEE':['KC', 'Coffee'],
                'LUMBER':['LB', 'Lumber'],
                'SUGAR':['SB', 'Sugar'],
                '30YB':['ZB', '30 Year Bond'],
                '10YN':['ZN', '10 Year Note'],
                '5YN':['ZF', '5 Year Note'],
                '2YN':['ZT', '2 Year Note'],       
                'USD':['DX', 'USD'],                   
                }

DICT_FINVIZ_CRYPTO = {
                'BTC':['BTCUSD', 'BTC/USD'],   
                'LTC':['LTCUSD', 'LTC/USD'],   
                'ETH':['ETHUSD', 'ETH/USD'],   
                'XRP':['XRPUSD', 'XRP/USD'],                
                }

def get_futures_chart(code, period):

    if (period == "M"):
        p = "m1"
    elif (period == "m"):
        p = "m5"
    else:
        p = period + "1"

    return "https://finviz.com/fut_chart.ashx?t=%s&p=%s" % (code.upper(),  p)

def get_crypto_chart(code, period):

    if (period == "M"):
        p = "m1"
    elif (period == "m"):
        p = "m5"
    else:
        p = period + "1"

    return "https://finviz.com/fx_image.ashx?%s_%s_l.png" % (code.lower(),  p)

def is_finviz_code(code):

    if (code.upper() in DICT_FINVIZ_FUTURES or code.upper() in DICT_FINVIZ_CRYPTO):
        return True
    else:
        return False

def get_finviz_chart(code, period):

    code = code.upper()
    if code in DICT_FINVIZ_FUTURES:
        return get_futures_chart(DICT_FINVIZ_FUTURES[code][0], period)
    elif code in DICT_FINVIZ_CRYPTO:
        return get_crypto_chart(DICT_FINVIZ_CRYPTO[code][0], period)

    return None    

def main():

    for code in ["BTC","NIKKEI","LTC","30YB"]:
        print(get_finviz_chart(code, "d"))
    #print(get_futures_chart("YM", "d"))
    #print(get_crypto_chart("BTCUSD", "d"))

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              
