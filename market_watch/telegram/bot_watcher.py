#!/usr/bin/python

# django shell import
import os
import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from decimal import Decimal
import urllib.request
import urllib.error
from socket import timeout
import random
import resource

from market_watch.common.AastocksEnum import TimeFrame, FxCode, IndexCode
from market_watch.common.AastocksConstants import *

from market_watch.yahoo import worldindices
from market_watch.dailyfx import market_calendar
from market_watch.aastocks import top_yield, charting, company_news, result_announcement, indices, forex, futures, company_profile
from market_watch.stockq import commodities
from market_watch.eastmoney import commodities as sina_commodities
from market_watch.fxcm import live_rate
from market_watch.hkex import ccass_loader
from market_watch.google import stock_history
from market_watch.sl886 import hkadr
from market_watch.alpha import analysis_loader
from market_watch.fool import fool_loader
from market_watch.qq import us_company_news
from market_watch.twitter import tweet
from market_watch.finviz import charting as fcharting
from market_watch.cnn import ust
from market_watch.quantum import tickersearch
from market_watch.bondsupermart import tickersearch as super_tickersearch

from market_watch.util import config_loader
from market_watch import quick_list, quick_tracker

from hickory.crawler.aastocks import stock_quote
from hickory.crawler.iextrading import stock_quote as iex_stock_quote
from hickory.crawler.alphavantage import fx_quote
from hickory.crawler.hkex import mutual_market
from hickory.crawler.wsj import jp_stock_quote

# Load static properties
config = config_loader.load()

# Redirect stdout to file
#old_stdout = sys.stdout
#sys.stdout = open("xxxx.log", 'w')

DICT_CURRENCY = {'BTC':'BTCUSD', 'ETH':'ETHUSD', 'XRP':'XRPUSD',
                 'LTC':'LTCUSD', 'EUR':'EURUSD', 'GBP':'GBPUSD',
                 'AUD':'AUDUSD', 'NZD':'NZDUSD', 'JPY':'USDJPY',
                 'CAD':'USDCAD', 'HKD':'USDHKD', 'CHF':'USDCHF',
                 'SGD':'USDSGD', 'CNY':'USDCNY', 'CNYHKD':'CNYHKD',
                 'EURGBP':'EURGBP','HKDJPY':'HKDJPY', 'EURHKD':'EURHKD',
                 'GBPHKD':'GBPHKD', 'AUDHKD':'AUDHKD'}

MAX_MSG_SIZE = 4096
                 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    print("Text Command: " + msg['text'])
    
    command = msg['text'].split("@")[0]
    
    keyboard_list = []
    reply = ""
    
    if (command == "/fx"):
        keyboard_list = [
                       [InlineKeyboardButton(text='EURUSD', callback_data='EURUSD'), InlineKeyboardButton(text='GBPUSD', callback_data='GBPUSD'), InlineKeyboardButton(text='USDJPY', callback_data='USDJPY')],
                       [InlineKeyboardButton(text='AUDUSD', callback_data='AUDUSD'), InlineKeyboardButton(text='NZDUSD', callback_data='NZDUSD'), InlineKeyboardButton(text='USDCAD', callback_data='USDCAD')],
                       [InlineKeyboardButton(text='USDCHF', callback_data='USDCHF'), InlineKeyboardButton(text='EURJPY', callback_data='EURJPY'), InlineKeyboardButton(text='GBPJPY', callback_data='GBPJPY')],
                       [InlineKeyboardButton(text='EURGBP', callback_data='EURGBP'), InlineKeyboardButton(text='AUDNZD', callback_data='AUDNZD'), InlineKeyboardButton(text='USDCNH', callback_data='USDCNH')],
                       [InlineKeyboardButton(text='DXY', callback_data='DXY')]
               ]
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
        bot.sendMessage(chat_id, 'Please tap on the FX pair to quote', reply_markup=keyboard)
        
    elif (command == "/idq"):
        keyboard_list = [
                       [InlineKeyboardButton(text='HSI', callback_data='HKG33'), InlineKeyboardButton(text='NIKKEI', callback_data='JPN225'), InlineKeyboardButton(text='DJI', callback_data='US30')],
                       [InlineKeyboardButton(text='SPX', callback_data='SPX500'), InlineKeyboardButton(text='NASDAQ', callback_data='NAS100'), InlineKeyboardButton(text='FTSE', callback_data='UK100')],
                       [InlineKeyboardButton(text='DAX', callback_data='GER30'), InlineKeyboardButton(text='IBEX', callback_data='ESP35'), InlineKeyboardButton(text='CAC', callback_data='FRA40')],
                       [InlineKeyboardButton(text='S&P/ASX 200', callback_data='AUS200'), InlineKeyboardButton(text='Euro Stoxx 50', callback_data='EUSTX50'), InlineKeyboardButton(text='Bund', callback_data='Bund')],
               ]
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
        bot.sendMessage(chat_id, 'Please tap on the Index to quote', reply_markup=keyboard)
        
    elif (command == "/cmd"):
        keyboard_list = [
                       [InlineKeyboardButton(text='WTI Crude', callback_data='USOil'), InlineKeyboardButton(text='Brent Oil', callback_data='UKOil'), InlineKeyboardButton(text='Gold', callback_data='XAUUSD')],
                       [InlineKeyboardButton(text='Silver', callback_data='XAGUSD'), InlineKeyboardButton(text='Natural Gas', callback_data='NGAS'), InlineKeyboardButton(text='Copper', callback_data='Copper')],
               ]
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_list)
        bot.sendMessage(chat_id, 'Please tap on the Commodity to quote', reply_markup=keyboard) 

    elif (command == "/live"):
        
        bot.sendMessage(chat_id, live_rate.get_full_live_rate(), parse_mode='HTML')
    
    elif (command == "/trump"):
    
        bot.sendMessage(chat_id, tweet.trump(5), parse_mode='HTML')

    elif (command.startswith("/twt")):
    
        action = None
        params = None
 
        try:            
            params = command[4:]
            params = params.split(" ")
        except:
            params = []
            
        print("Param: " + str(params))
    
        if (params):
            bot.sendMessage(chat_id, tweet.get_tweet(params[0], 5), parse_mode='HTML')
        
    elif (command == "/top10"):
    
        menuitemlist = [{'command': '/ttETF', 'desc': 'High Dividends ETF', 'icon': u'\U0001F4B0'},
                    {'command': '/ttBanks', 'desc': 'High Dividends Banks', 'icon': u'\U0001F3E6'},
                    {'command': '/ttREIT', 'desc': 'High Dividends REIT', 'icon': u'\U0001F3E2'},
                    {'command': '/ttCong', 'desc': 'High Dividends Conglomerates', 'icon': u'\U0001F310'},
        ]
 
        passage = 'Please tap on the Top 10 list to show '
        
        for menuitem in menuitemlist:
            passage = passage + DEL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
 
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
      
    elif (command == "/cal"):
    
        bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')
        passage = market_calendar.get_fx_calendar()
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
    
    elif (command.startswith("/t")):

        action = None
        params = None
 
        try:            
            action = command[2:3]
            params = command[3:]
            params = params.split(" ")
        except:
            params = []
            
        print("Action: " + action)
        print("Param: " + str(params))
    
        # for top ten categories list
        if (action=="t"):
    
            bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')        
            industry = command[3:]
            
            if (industry == "ETF"):
                passage = top_yield.get_etf_stat(config.get("aastocks","hy-url-etf"))
            elif (industry == "Banks"):
                passage = top_yield.get_hy_stat(config.get("aastocks-hy-industry","hy-url-banks"), "Banks")
            elif (industry == "REIT"):
                passage = top_yield.get_hy_stat(config.get("aastocks-hy-industry","hy-url-reits"), "REIT")
            elif (industry == "Cong"):   
                passage = top_yield.get_hy_stat(config.get("aastocks-hy-industry","hy-url-conglomerates"), "Conglomerates")
            else:
                passage = '<i>Sorry! Top 10 List not found for target [' + industry + '] </i>'
                
            passage = passage + 'Back to Top 10 Menu - /top10'
            bot.sendMessage(chat_id, passage, parse_mode='HTML')
        
        elif (action=="l"):
            print(quick_tracker.list_track())
            bot.sendMessage(chat_id, quick_tracker.list_track(), parse_mode='HTML')   
            
        elif (action=="a"):
            passage = ""
            for code in params:
                code = code.upper()
                if (quick_tracker.add_track(code)):
                    passage = passage + code + " add successfully." + EL
                else:
                    passage = passage + code + " add failed." + EL
            print(passage)        
            if (passage):
                bot.sendMessage(chat_id, passage, parse_mode='HTML')
                
        elif (action=="d"):
            passage = ""
            for code in params:
                code = code.upper()
                if (quick_tracker.remove_track(code)):
                    passage = passage + code + " remove successfully." + EL
                else:
                    passage = passage + code + " remove failed." + EL
            print(passage)        
            if (passage):
                bot.sendMessage(chat_id, passage, parse_mode='HTML')

        elif (action=="h"):
            passage = ""
            for code in params:
                code = code.upper()
                if (quick_tracker.mark_track(code)):
                    passage = passage + code + " mark successfully." + EL
                else:
                    passage = passage + code + " mark failed." + EL
            print(passage)        
            if (passage):
                bot.sendMessage(chat_id, passage, parse_mode='HTML')
    
    elif (command.startswith("/l")):

        try:
            action = command[2:]
        except IndexError:
            action = ""

        print("Action: [" + action + "]") 

        menu = '<b>Live Command</b> ' + u'\U0001F4C8'

        menuitemlist = [{'command': '/lhk', 'desc': 'HK Indices', 'icon': u'\U0001F4C8'},
                    {'command': '/lcn', 'desc': 'CN Indices', 'icon': u'\U0001F4C8'},
                    {'command': '/lw', 'desc': 'World Indices', 'icon': u'\U0001F4C8'},
                    {'command': '/lm', 'desc': 'Commodities and Metals', 'icon': u'\U0001F4C8'},
                    {'command': '/lfx', 'desc': 'Forex', 'icon': u'\U0001F4C8'},
        ]

        for menuitem in menuitemlist:
            menu = menu + DEL + ' ' + menuitem['command'] + ' - ' + menuitem['desc']
            
        if (action == "hk"):
            bot.sendMessage(chat_id, indices.get_indices("hk"), parse_mode='HTML') 
        elif (action == "cn"):
            bot.sendMessage(chat_id, indices.get_indices("cn"), parse_mode='HTML') 
        elif (action == "w"):
             bot.sendMessage(chat_id, worldindices.get_indices(), parse_mode='HTML') 
        elif (action == "fx"):
            bot.sendMessage(chat_id, forex.get_forex(), parse_mode='HTML')
        elif (action == "adr"):
            bot.sendMessage(chat_id, hkadr.get_hkadr(), parse_mode='HTML') 
        elif (action == "m"):
            bot.sendMessage(chat_id, commodities.get_commodities(), parse_mode='HTML') 
            bot.sendMessage(chat_id, sina_commodities.get_commodities(), parse_mode='HTML') 
        elif (action == "l"):
            msg = "<a href='http://eggyolk.tech/heatmap.html' target='_blank'>Chicken Heatmap (HK)</a>" + DEL
            msg = msg + "<a href='http://eggyolk.tech/heatmap_us.html' target='_blank'>Chicken Heatmap (US)</a>" + DEL
            msg = msg + "<a href='http://eggyolk.tech/y8.html' target='_blank'>Y8 List (HK)</a>" + DEL
            msg = msg + "<a href='http://eggyolk.tech/y8_us.html' target='_blank'>Y8 List (US)</a>" + DEL
            msg = msg + "<a href='http://eggyolk.tech/moneyflow.html' target='_blank'>Southbound Moneyflow Track</a>" + DEL

            bot.sendMessage(chat_id, msg, parse_mode='HTML')
        else:        
            bot.sendMessage(chat_id, menu, parse_mode='HTML') 

        return   
         
    elif (command.startswith("/q")):
    
        try:            
            cmds = command.split(' ')
            quote = cmds[0]
            params = cmds[1:]
        except IndexError:
            params = ""
            
        print("Quote: " + quote)
        print("Param: " + str(params))
    
        action = quote[2:3]
        code = quote[3:]
        codes = [code] + cmds[1:]
        print(codes)       
 
        menu = '<b>Quick Quote Command</b> ' + u'\U0001F4C8'
        
        menuitemlist = [{'command': '/qM[code] [option]', 'desc': 'Monthly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qw[code] [option]', 'desc': 'Weekly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qd[code] [option]', 'desc': 'Daily Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qh[code] [option]', 'desc': 'Hourly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qm[code] [option]', 'desc': 'Minutes Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qa[us_code]', 'desc': 'Seeking Alpha (US only)', 'icon': u'\U0001F414'},    
                    {'command': '/qA[us_code]', 'desc': 'Motley Fool (US only)', 'icon': u'\U0001F414'},   
                    {'command': '/qb[ticker]', 'desc': 'bondsupermart Search', 'icon': u'\U0001F414'},   
                    {'command': '/qB[us_ticker]', 'desc': 'XTBs List (US only)', 'icon': u'\U0001F414'},   
                    {'command': '/qC[code]', 'desc': 'CCASS Top 10 Distribution', 'icon': u'\U0001F42E'},
                    {'command': '/qc', 'desc': 'CBBC Distribution', 'icon': u'\U0001F42E'},
                    {'command': '/qe[code]', 'desc': 'Southbound Moneyflow Trend', 'icon': u'\U0001F42E'},            
                    {'command': '/qf [next] [hscei] [night]', 'desc': 'Quote HSI Mini Futures', 'icon': u'\U0001F414'},
                    {'command': '/qF [next] [hscei] [night]', 'desc': 'Quote HSI Futures', 'icon': u'\U0001F414'},                   
                    {'command': '/qj[jp_code]', 'desc': 'Tokyo Stock Quote', 'icon': u'\U0001F414'}, 
                    {'command': '/qN[code]', 'desc': 'Result Calendar (HK Only)', 'icon': u'\U0001F4C8'},                    
                    {'command': '/qn[code]', 'desc': 'Latest News (HK Only)', 'icon': u'\U0001F4C8'},                    
                    {'command': '/qq', 'desc': 'Quick Quote', 'icon': u'\U0001F42E'},
                    {'command': '/qp', 'desc': 'Dividenc & OCF History', 'icon': u'\U0001F42E'},
                    {'command': '/qR', 'desc': 'Industries List', 'icon': u'\U0001F42E'},
                    {'command': '/qr[code1] [code2]', 'desc': 'Relative Strength', 'icon': u'\U0001F42E'},
                    {'command': '/qs', 'desc': 'Chicken Sectormap', 'icon': u'\U0001F414'},
                    {'command': '/qS[code]', 'desc': 'Get Company Profile', 'icon': u'\U0001F414'},
                    {'command': '/qY', 'desc': 'Treasury Yield', 'icon': u'\U0001F414'}, 
                    {'command': '/l', 'desc': 'Live Quote Commands', 'icon': u'\U0001F414'},
        ]
        
        fxc = ", ".join(['/qh' + str(x.name) for x in FxCode][:3])
        idxc = ", ".join(['/qd' + str(x.name) for x in IndexCode][:3])

        for menuitem in menuitemlist:
            menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc']
        
        menu = menu + DEL + "[option]: bb - Bollinger Band, sma - SMA"
        
        menu = menu + DEL + "<b>Sample</b>"
        menu = menu + EL + "Stock: /qd5, /qm601318, /qMAAPL, /qwMCD"   
        menu = menu + EL + "FX: " + fxc
        menu = menu + EL + "Index: " + idxc  
        menu = menu + EL + "News / CCASS: /qn5, /qn3333, /qC606"     
        menu = menu + EL + "Profile (HK): /qS5, /qS981"     
        menu = menu + EL + "Southbound Moneyflow: /qe5, /qe581"     
        menu = menu + EL + "Rel Strength: /qr5 2388 3988, /qR (by sectors)"           
        
        if (action in ["M", "w", "W", "d", "D", "h", "H", "m"]):
        
            # Bucket Scenario to display stock chart
            if code:
            
                if(is_white_listed(chat_id)):
                    print("White Listed: [" + str(chat_id) + "]")        
                    bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')
                    
                    linklist = charting.get_hkg_chart_list_by_type(code, action, params)
                    
                    for link_dict in linklist:
                        try:
                            f = urllib.request.urlopen(link_dict['url'], timeout=10)
                        except:
                            bot.sendMessage(chat_id, u'\U000026D4' + ' Request Timeout for [' + link_dict['code'] + ']', parse_mode='HTML')
                        else:
                            bot.sendPhoto(chat_id, f)
                else:
                    print("Not in White List: [" + str(chat_id) + "]")
                    bot.sendMessage(chat_id, u'\U000026D4' + ' Request Timeout', parse_mode='HTML')
            else:

                stockcode = random.choice(["2628", "939", "2800", "8141", "AAPL", "GOOG", "GS"])
                p1 = "<i>Usage:</i> " + command.split(' ')[0] + "[StockCode] (e.g. " + command.split(' ')[0] + stockcode + ")"

                p2 = "<i>Sample (Futures):</i>" + EL
                for fCode in fcharting.DICT_FINVIZ_FUTURES:
                    p2 = p2 + command.split(' ')[0] + fCode + " - " + fcharting.DICT_FINVIZ_FUTURES[fCode][1] + EL

                p3 = "<i>Sample (Crypto):</i>" + EL
                for fCode in fcharting.DICT_FINVIZ_CRYPTO:
                    p3 = p3 + command.split(' ')[0] + fCode + " - " + fcharting.DICT_FINVIZ_CRYPTO[fCode][1] + EL

                passage = random.choice([p1, p2, p3])
                bot.sendMessage(chat_id, passage, parse_mode='HTML')

        elif (action == "A"):

            if (is_number(code)):
                bot.sendMessage(chat_id, "Only US Stock is supported", parse_mode='HTML')
            else:
                rhtml = fool_loader.get_analysis(code)
                bot.sendMessage(chat_id, rhtml, parse_mode='HTML')
            return
                
        elif (action == "a"):

            if (is_number(code)):
                bot.sendMessage(chat_id, "Only US Stock is supported", parse_mode='HTML')
            else:
                rhtml = analysis_loader.get_analysis(code)
                bot.sendMessage(chat_id, rhtml, parse_mode='HTML')
            return

        elif (action == "B"):

            if (is_number(code)):
                bot.sendMessage(chat_id, "Only US Stock is supported", parse_mode='HTML')
            else:
                bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML') 
                message = tickersearch.get_sec_list(code)
                bot.sendMessage(chat_id, message, parse_mode='HTML')
            return            

        elif (action == "b"):

            if (is_number(code)):
                bot.sendMessage(chat_id, "Only Ticker Symbol is supported", parse_mode='HTML')
            else:
                bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML') 
                message = super_tickersearch.get_sec_list(code)
                bot.sendMessage(chat_id, message, parse_mode='HTML')
            return            
            
        elif (action == "c"):

            bot.sendMessage(chat_id, u'\U0001F42E' +  u'\U0001F43B' + u'\U0001F4CA', parse_mode='HTML')
            
            try:
                f = urllib.request.urlopen(config.get("credit-suisse","cbbc-url"), timeout=10)
            except:
                bot.sendMessage(chat_id, u'\U0001F428' + ' Request Timeout', parse_mode='HTML')
            else:
                bot.sendPhoto(chat_id, f)                
            return    
            
        elif (action == "C"):
            bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')         
            bot.sendMessage(chat_id, ccass_loader.get_latest_ccass_info(code, 20) , parse_mode='HTML')
            bot.sendMessage(chat_id, ccass_loader.get_shareholding_disclosure(code) , parse_mode='HTML')
            return

        elif (action == "e"):
            bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')         
        
            for stockCd in codes:
                bot.sendMessage(chat_id, mutual_market.get_moneyflow_by_code(stockCd), parse_mode='HTML')
            return            
            
        elif (action == "f"):
            bot.sendMessage(chat_id, futures.get_futures("M", params), parse_mode='HTML')
            return

        elif (action == "F"):
            bot.sendMessage(chat_id, futures.get_futures("N", params), parse_mode='HTML')
            return
        
        elif (action.lower() == "j"):

            # Get quick quote from WSJ
            simpleMode = True
            if (action == "J"):
                simpleMode = False
            
            for stockCd in codes:
                if (stockCd.strip().isdigit() and len(stockCd.strip()) == 4):
                    bot.sendMessage(chat_id, jp_stock_quote.get_quote_message(stockCd, simpleMode), parse_mode='HTML')
                else:
                    bot.sendMessage(chat_id, "Invalid JP Stock Code: [%s]" % stockCd, parse_mode='HTML')
                    
        elif (action == "N"):
            bot.sendMessage(chat_id, result_announcement.get_result_calendar(code), parse_mode='HTML')                    

        elif (action == "n"):

            if (is_number(code)):
                bot.sendMessage(chat_id, company_news.get_latest_news_by_code(code, 8), parse_mode='HTML')
            else:
                bot.sendMessage(chat_id, us_company_news.get_latest_news_by_code(code, 10), parse_mode='HTML')
            return    
        
        elif (action == "p"):

            if (is_number(code)):
                bot.sendMessage(chat_id, company_profile.get_dividend(code), parse_mode='HTML')
                bot.sendMessage(chat_id, company_profile.get_ocf(code), parse_mode='HTML')
            else:
                bot.sendMessage(chat_id, "Only HK Stock is supported", parse_mode='HTML')
            return    
 
        elif (action.lower() == "q"):

            # Get quick quote from AAStocks
            simpleMode = True
            if (action == "Q"):
                simpleMode = False
            
            for stockCd in codes:
                if (stockCd.strip().isdigit() and len(stockCd.strip()) == 6):
                    bot.sendMessage(chat_id, stock_quote.get_quote_message(stockCd, "CN", simpleMode), parse_mode='HTML')
                elif (stockCd.strip().isdigit()):
                    bot.sendMessage(chat_id, stock_quote.get_quote_message(stockCd, "HK", simpleMode), parse_mode='HTML')
                elif (stockCd.strip()):

                    if (stockCd.upper() in DICT_CURRENCY):
                        fromCur = DICT_CURRENCY[stockCd.upper()][0:3]
                        toCur = DICT_CURRENCY[stockCd.upper()][3:6]
                        bot.sendMessage(chat_id, fx_quote.get_fx_quote_message(fromCur, toCur), parse_mode='HTML')
                    else:
                        bot.sendMessage(chat_id, iex_stock_quote.get_quote_message(stockCd, "US", simpleMode), parse_mode='HTML')
                #else:
                #    bot.sendMessage(chat_id, u'\U000026D4' + ' Code Not found!', parse_mode='HTML')
 
        elif (action == "R"):
            
            if (not code):
                bot.sendMessage(chat_id, stock_history.get_stocks_rs_industry_list(), parse_mode='HTML') 
                return
            elif (code):
                
                # getting top 10 stock list within industry first
                result = stock_history.get_stocks_rs_list(code.strip(), 20)
                passage = result[0]
                codelist = result[1]
                
                if (len(codelist) > 0):
                    bot.sendMessage(chat_id, passage, parse_mode='HTML')
                else:
                    bot.sendMessage(passage)
                    return
                
                # generating RS charts accordingly
                bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')
                try:
                    print("Chart Code List: [" + str(codelist) + "]")
                    result = stock_history.get_stocks_rs_charts(codelist)
                    chartpath = result[0]
                    invalidcodelist = result[1]
                    print("Chart Path: [" + chartpath + "]")

                except Exception as e:
                    print("Exception raised: [" + str(e) +  "]")
                    bot.sendMessage(chat_id, u'\U000026D4' + ' ' + str(e), parse_mode='HTML')
                else:
                    if(len(invalidcodelist) > 0):
                        bot.sendMessage(chat_id, u'\U000026D4' + " Stocks with no data: " + str(invalidcodelist) , parse_mode='HTML')
                    bot.sendPhoto(chat_id=chat_id, photo=open(chartpath, 'rb'))
                return               
            
        elif (action == "r"):
            bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')         
            try:
                #print(str([code] + params))
                result = stock_history.get_stocks_rs_charts([code] + params)
                chartpath = result[0]
                invalidcodelist = result[1]
                print("Chart Path: [" + chartpath + "]")

            except Exception as e:
                print("Exception raised: [" + str(e) +  "]")
                bot.sendMessage(chat_id, u'\U000026D4' + ' ' + str(e), parse_mode='HTML')
            else:
                if(len(invalidcodelist) > 0):
                    bot.sendMessage(chat_id, u'\U000026D4' + " Stocks with no data: " + str(invalidcodelist) , parse_mode='HTML')
                bot.sendPhoto(chat_id=chat_id, photo=open(chartpath, 'rb'))      
            return
            
        elif (action == "S"):
            passage = company_profile.get_profile(code)

            results = [passage[i:i+MAX_MSG_SIZE] for i in range(0, len(passage), MAX_MSG_SIZE)]

            for result in results:
                bot.sendMessage(chat_id, result, parse_mode='HTML')
        elif (action == "s"):

            bot.sendMessage(chat_id, u'\U0001F414' +  u'\U0001F413' + u'\U0001F4B9', parse_mode='HTML')
            
            try:
                f = urllib.request.urlopen("http://www.fafaworld.com/usectors.jpg", timeout=10)
            except:
                bot.sendMessage(chat_id, u'\U0001F423' + ' Request Timeout', parse_mode='HTML')
            else:
                bot.sendPhoto(chat_id, f)                
            return                 
    
        elif (action == "Y"):
            result = ust.get_ust_yield()
            
            if (result):
                bot.sendMessage(chat_id, result[0], parse_mode='HTML')

                try:
                    f = urllib.request.urlopen(result[1], timeout=10)
                except:
                    pass
                else:
                    bot.sendPhoto(chat_id, f)
            else:
                bot.sendMessage(chat_id, u'\U0001F423' + ' Request Error', parse_mode='HTML')
        
        else:        
            bot.sendMessage(chat_id, menu, parse_mode='HTML') 
            return
        
    elif (command.startswith("/")):    
    
        menuitemlist = [{'command': '/fx', 'desc': 'FX Quote', 'icon': u'\U0001F4B9'},
                        {'command': '/idq', 'desc': 'Index Quote', 'icon': u'\U0001F310'},
                        {'command': '/cmd', 'desc': 'Commodities Quote', 'icon': u'\U0001F30E'},
                        {'command': '/cal', 'desc': 'Coming Market Events', 'icon': u'\U0001F4C5'},
                        {'command': '/top10', 'desc': 'Top 10 List', 'icon': u'\U0001F51F'},
                        {'command': '/trump', 'desc': 'Trump Trump tweet', 'icon': u'\U0001F51F'},
                        {'command': '/twt [screen_name]', 'desc': 'Get Twitter Tweets', 'icon': u'\U0001F51F'},                        
                        {'command': '/q', 'desc': 'Quick Command', 'icon': u'\U0001F4C8'},
        ]
        
        menu = '金鑊鏟 Bot v2.0 '
        
        for menuitem in menuitemlist:
            menu = menu + DEL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
    
        bot.sendMessage(chat_id, menu, parse_mode='HTML')
        
    else: 
        print("DO NOTHING for non / command")

def is_white_listed(in_chat_id):
    
    chat_list = config.items("telegram-chart")
    
    for key, chat_id in chat_list:
        #print("Compare: " + str(chat_id) + " <=> " + str(in_chat_id));
        if (str(in_chat_id) == str(chat_id)):
            return True;
    
    return False;
        
def on_callback_query(msg):

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    result = "No live rate is available"

    # if query data is available
    if query_data:
    
        if query_data == "DXY":
            result = query_data + ": " + live_rate.get_dxy_live_rate()
        else:  
            result = query_data + ": " + live_rate.get_fx_live_rate(query_data)
        
        bot.answerCallbackQuery(query_id, text=result)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
TOKEN = config.get("telegram","bot-id") # get token from command-line

# Set resource limit
rsrc = resource.RLIMIT_DATA
soft, hard = resource.getrlimit(rsrc)
print('Soft limit start as :' + str(soft))

resource.setrlimit(rsrc, (220 * 1024, hard))
soft, hard = resource.getrlimit(rsrc)

print('Soft limit start as :' + str(soft))

bot = telepot.Bot(TOKEN)
print(bot.getMe())
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)
 
