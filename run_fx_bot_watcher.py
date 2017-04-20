# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricewatch.settings")
django.setup()

from pricealert.models import PriceAlert
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
from get_daily_fx_calendar import get_fx_calendar
from get_aastocks_hy_stats import get_aastocks_etf_stat, get_aastocks_hy_stat
from get_fx_live_rate import get_fx_live_rate, get_dxy_live_rate
from get_aastocks_chart import get_hkg_chart_by_type
from get_aastocks_news import get_latest_news_by_code
from get_hkex_ccass_info import get_latest_ccass_info
from get_quick_list import get_qq_command_list, get_qq_command_tf_list, get_qq_command_detail_list
from get_yahoo_stock_info import get_stocks_rs_charts, get_stocks_rs_industry_list, get_stocks_rs_list
import configparser

from classes.AastocksEnum import TimeFrame, FxCode, IndexCode
from classes.AastocksConstants import *

config = configparser.ConfigParser()
config.read('config.properties')

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
        passage = get_fx_calendar()
        bot.sendMessage(chat_id, passage, parse_mode='HTML')
    
    elif (command.startswith("/tt")):
    
        bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')
        
        industry = command[3:]
        
        if (industry == "ETF"):
            passage = get_aastocks_etf_stat(config.get("aastocks","hy-url-etf"))
        elif (industry == "Banks"):
            passage = get_aastocks_hy_stat(config.get("aastocks-hy-industry","hy-url-banks"), "Banks")
        elif (industry == "REIT"):
            passage = get_aastocks_hy_stat(config.get("aastocks-hy-industry","hy-url-reits"), "REIT")
        elif (industry == "Cong"):   
            passage = get_aastocks_hy_stat(config.get("aastocks-hy-industry","hy-url-conglomerates"), "Conglomerates")
        else:
            passage = '<i>Sorry! Top 10 List not found for target [' + industry + '] </i>'
            
        passage = passage + 'Back to Top 10 Menu - /top10'
        bot.sendMessage(chat_id, passage, parse_mode='HTML') 

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
        
        menu = '<b>Quick Quote Command</b> ' + u'\U0001F4C8'
        
        menuitemlist = [{'command': '/qM[code] [option]', 'desc': 'Monthly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qw[code] [option]', 'desc': 'Weekly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qd[code] [option]', 'desc': 'Daily Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qh[code] [option]', 'desc': 'Hourly Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qm[code] [option]', 'desc': 'Minutes Chart', 'icon': u'\U0001F4C8'},
                    {'command': '/qn[code]', 'desc': 'Latest News (HK Only)', 'icon': u'\U0001F4C8'},                    
                    {'command': '/qC[code]', 'desc': 'CCASS Top 10 Distribution', 'icon': u'\U0001F42E'},
                    {'command': '/qc', 'desc': 'CBBC Distribution', 'icon': u'\U0001F42E'},
                    {'command': '/qr[code1] [code2]', 'desc': 'Relative Strength', 'icon': u'\U0001F42E'},
                    {'command': '/qq', 'desc': 'Quick Menu', 'icon': u'\U0001F42E'},
        ]
        
        fxc = ", ".join(['/qh' + str(x.name) for x in FxCode][:3])
        idxc = ", ".join(['/qd' + str(x.name) for x in IndexCode][:3])

        for menuitem in menuitemlist:
            menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc']
        
        menu = menu + DEL + "[option]: bb - Show Bollinger Bands"
        
        menu = menu + DEL + "<b>Sample</b>"
        menu = menu + EL + "Stock: /qd5, /qm601318, /qMAAPL, /qwMCD"   
        menu = menu + EL + "FX: " + fxc
        menu = menu + EL + "Index: " + idxc  
        menu = menu + EL + "News / CCASS: /qn5, /qn3333, /qC606"     
        menu = menu + EL + "Rel Strength: /qr5 2388"           
        
        if (action in ["M", "w", "W", "d", "D", "h", "H", "m"]):
        
            # Bucket Scenario to display stock chart
            if code:
            
                if(is_white_listed(chat_id)):
                    print("White Listed: [" + str(chat_id) + "]")        
                    bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')
                    
                    try:
                        f = urllib.request.urlopen(get_hkg_chart_by_type(code, action, params), timeout=10)
                    except:
                        bot.sendMessage(chat_id, u'\U000026D4' + ' Request Timeout', parse_mode='HTML')
                    else:
                        bot.sendPhoto(chat_id, f)
                else:
                    print("Not in White List: [" + str(chat_id) + "]")
                    bot.sendMessage(chat_id, u'\U000026D4' + ' Request Timeout', parse_mode='HTML')
            else:
                stockcode = random.choice(["2628", "939", "2800", "8141", "AAPL", "GOOG", "GS"])
                passage = "<i>Usage:</i> " + command.split(' ')[0] + "[StockCode] (e.g. " + command.split(' ')[0] + stockcode + ")"
                bot.sendMessage(chat_id, passage, parse_mode='HTML')
   
        elif (action.lower() == "n"):
            bot.sendMessage(chat_id, get_latest_news_by_code(code, 8), parse_mode='HTML')
            return    
            
        elif (action == "C"):
            bot.sendMessage(chat_id, random.choice(LOADING), parse_mode='HTML')         
            bot.sendMessage(chat_id, get_latest_ccass_info(code, 10) , parse_mode='HTML')
            return

        elif (action == "R"):
            
            if (not code):
                bot.sendMessage(chat_id, get_stocks_rs_industry_list(), parse_mode='HTML') 
                return
            elif (code):
                
                # getting top 10 stock list within industry first
                result = get_stocks_rs_list(code.strip(), 12)
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
                    result = get_stocks_rs_charts(codelist)
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
                chart = get_stocks_rs_charts([code] + params)
                print("Chart Path: [" + chart + "]")

            except Exception as e:
                print("Exception raised: [" + str(e) +  "]")
                bot.sendMessage(chat_id, u'\U000026D4' + ' ' + str(e), parse_mode='HTML')
            else:
                bot.sendPhoto(chat_id=chat_id, photo=open(chart, 'rb'))      
            return
            
        elif (action == "c"):

            bot.sendMessage(chat_id, u'\U0001F42E' +  u'\U0001F43B' + u'\U0001F4CA', parse_mode='HTML')
            
            try:
                f = urllib.request.urlopen(config.get("credit-suisse","cbbc-url"), timeout=10)
            except:
                bot.sendMessage(chat_id, u'\U000026D4' + ' Request Timeout', parse_mode='HTML')
            else:
                bot.sendPhoto(chat_id, f)                
            return                 
        elif (action.lower() == "q"):
        
            if (code in QQLIST):
                bot.sendMessage(chat_id, get_qq_command_list(code) , parse_mode='HTML')
                return
            elif (code[0:5] in QQSUBLIST):
                bot.sendMessage(chat_id, get_qq_command_detail_list(code) , parse_mode='HTML')
                return
            elif (code):
                bot.sendMessage(chat_id, get_qq_command_tf_list(code) , parse_mode='HTML')
                return
            else:
                passage = "<i>Use the following shortcuts to list quote items:</i> " + DEL
                for list in QQLIST:
                    passage = passage + "/qq" + list +  EL + " - List " + list + " codes" + EL
                    
                bot.sendMessage(chat_id, passage, parse_mode='HTML')
                return
        else:        
            bot.sendMessage(chat_id, menu, parse_mode='HTML') 
            return
        
    elif (command.startswith("/")):    
    
        menuitemlist = [{'command': '/fx', 'desc': 'FX Quote', 'icon': u'\U0001F4B9'},
                        {'command': '/idq', 'desc': 'Index Quote', 'icon': u'\U0001F310'},
                        {'command': '/cmd', 'desc': 'Commodities Quote', 'icon': u'\U0001F30E'},
                        {'command': '/cal', 'desc': 'Coming Market Events', 'icon': u'\U0001F4C5'},
                        {'command': '/top10', 'desc': 'Top 10 List', 'icon': u'\U0001F51F'},
                        {'command': '/q', 'desc': 'Quick Command', 'icon': u'\U0001F4C8'},
        ]
        
        menu = '金鑊鏟 Bot v1.1.1'
        
        for menuitem in menuitemlist:
            menu = menu + DEL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
    
        bot.sendMessage(chat_id, menu, parse_mode='HTML')
        
    else: 
        print("DO NOTHING for non / command")

def is_white_listed(in_chat_id):
    
    chat_list = config.items("telegram-chat")
    
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
            result = query_data + ": " + get_dxy_live_rate()
        else:  
            result = query_data + ": " + get_fx_live_rate(query_data)
        
        bot.answerCallbackQuery(query_id, text=result)
    
TOKEN = config.get("telegram","bot-id") # get token from command-line

bot = telepot.Bot(TOKEN)
print(bot.getMe())
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)
 
