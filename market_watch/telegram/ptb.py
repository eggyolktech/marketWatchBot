#!/usr/bin/python3.7

from market_watch.util import config_loader
from market_watch.common.AastocksEnum import TimeFrame, FxCode, IndexCode
from market_watch.common.AastocksConstants import *
from market_watch.aastocks import (
    top_yield, 
    charting, 
    company_news, 
    result_announcement, 
    indices, 
    forex, 
    futures,        
    company_profile
)

from market_watch.dailyfx import market_calendar
from market_watch.stockq import commodities
from market_watch.sl886 import hkadr
from market_watch.yahoo import worldindices
from market_watch.etfdb import etf_info
from market_watch.fxcm import live_rate
from market_watch.hkex import options, options_report
from market_watch.finviz import heatmap, charting as fcharting
from market_watch.alpha import analysis_loader
from market_watch.hkex import ccass_loader
from market_watch.etfdb import etf_info
from market_watch.google import stock_history
from market_watch.finviz import heatmap, charting as fcharting
from market_watch.stockcharts import charting as scharting
from market_watch.cnn import ust

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from telegram import ParseMode
import io
import logging
import random
import resource
import datetime
import requests
from bs4 import BeautifulSoup
import traceback
import urllib.request
import urllib.error

from hickory.crawler.hkex import mutual_market
from hickory.crawler.aastocks import stock_quote
from hickory.crawler.iextrading import stock_quote as iex_stock_quote
from hickory.crawler.alphavantage import fx_quote
from hickory.crawler.cnyes import crypto_quote

################### Load static properties
#config = config_loader.load("DEV")
config = config_loader.load()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)

CRYPTO_CURRENCY = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH']

DICT_CURRENCY = {
                 'EUR':'EURUSD', 'GBP':'GBPUSD',
                 'AUD':'AUDUSD', 'NZD':'NZDUSD', 'JPY':'USDJPY',
                 'CAD':'USDCAD', 'HKD':'USDHKD', 'CHF':'USDCHF',
                 'SGD':'USDSGD', 'CNY':'USDCNY', 'CNYHKD':'CNYHKD',
                 'EURGBP':'EURGBP','HKDJPY':'HKDJPY', 'EURHKD':'EURHKD',
                 'GBPHKD':'GBPHKD', 'AUDHKD':'AUDHKD'}

MAX_MSG_SIZE = 4096

################### commmon functions

def is_white_listed(in_chat_id):
    
    chat_list = config.items("telegram-chart")
    
    for key, chat_id in chat_list:
        #print("Compare: " + str(chat_id) + " <=> " + str(in_chat_id));
        if (str(in_chat_id) == str(chat_id)):
            return True;
    
    return False;

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False    
    
################### send messages section
    
def sHTML(update, context, html):
    context.bot.send_message(chat_id=update.effective_chat.id, text=html, parse_mode=ParseMode.HTML)  
    
def sTEXT(update, context, text):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)  

def sIMAGE(update, context, img):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)  

def randomIcon(update, context):
    sHTML(update, context, random.choice(LOADING))    

def brokenIcon(update, context, errorMsg="I am afraid we are currently having problems"):
    sHTML(update, context, random.choice(BROKEN) + " " + errorMsg)

def unknown(update, context):
    sTEXT(update, context, "Sorry, I didn't understand that command.")    
    
def start(update, context):

    menu = '<b>金鑊鏟 Pre-Beta</b> ' + u'\U0001F4C8' + EL
    
    menuitemlist = [
                #{'command': '/cal', 'desc': 'Market Calendar', 'icon': u'\U0001F4C8'},
                {'command': '/l', 'desc': 'Live Quote Commands', 'icon': u'\U0001F414'},
                {'command': '/q', 'desc': 'Quick Quote Commands', 'icon': u'\U0001F4C8'},
                {'command': '/top10', 'desc': 'Top 10 Yieldings Stocks', 'icon': u'\U0001F4C8'},
    ]
    
    for menuitem in menuitemlist:
        menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc']
    
    sHTML(update, context, menu)
    
def test(update, context):
    text_caps = ' '.join(context.args).upper()
    img = 'https://pbs.twimg.com/profile_images/1354980830272253955/p2Z30z6j_200x200.jpg'
    sHTML(update, context, '<b>Flying to the moom!</b>')
    sIMAGE(update, context, img)

def textLog(update, context):
    if update.message:
        logger.info("from %s:[%s]" % (update.effective_chat.id, update.message.text))
    
def cal(update, context):

    randomIcon(update, context)
    sHTML(update, context, market_calendar.get_fx_calendar())

def top10(update, context):

    cmd = update.message.text
    cmd = cmd.split("@")[0] #remove bot suffix
    logger.info("from %s:[%s]" % (update.effective_chat.id, update.message.text))      
    passage = None
    
    if "/top10" == cmd:
   
        menuitemlist = [{'command': '/ttETF', 'desc': 'High Dividends ETF', 'icon': u'\U0001F4B0'},
                    {'command': '/ttBanks', 'desc': 'High Dividends Banks', 'icon': u'\U0001F3E6'},
                    {'command': '/ttREIT', 'desc': 'High Dividends REIT', 'icon': u'\U0001F3E2'},
                    {'command': '/ttCong', 'desc': 'High Dividends Conglomerates', 'icon': u'\U0001F310'},
        ]

        passage = 'Please tap on the Top 10 list to show '
        
        for menuitem in menuitemlist:
            passage = passage + DEL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']
    
        sHTML(update, context, passage)
    
    elif "/tt" in cmd:
    
        randomIcon(update, context)
        
        industry = cmd[3:]
        logger.info("industry:[%s]" % (industry))  
        passage = ""
            
        if (industry == "ETF"):
            passage = top_yield.get_etf_stat(config.get("aastocks","hy-url-etf"))
        elif (industry == "Banks"):
            passage = top_yield.get_hy_stat(config.get("aastocks-hy-industry","hy-url-banks"), "Banks")
        elif (industry == "REIT"):
            passage = top_yield.get_hy_stat(config.get("aastocks-hy-industry","hy-url-reits"), "REIT")
        elif (industry == "Cong"):   
            passage = top_yield.get_hy_stat(config.get("aastocks-hy-industry","hy-url-conglomerates"), "Conglomerates")

        passage = passage + 'Back to Top 10 Menu - /top10'
        sHTML(update, context, passage)          
    
    else:
        unknown(update, context)

def livequote(update, context):

    cmd = update.message.text
    cmd = cmd.split("@")[0] #remove bot suffix
    logger.info("from %s:[%s]" % (update.effective_chat.id, update.message.text))  
    
    if "/l" == cmd:

        passage = '<b>Live Quote Command</b> ' + u'\U0001F4C8' + EL
        menuitemlist = [{'command': '/lhk', 'desc': '香港指數', 'icon': u'\U0001F4C8'},
                    {'command': '/lcn', 'desc': '內地指數', 'icon': u'\U0001F4C8'},
                    {'command': '/lw', 'desc': '世界指數', 'icon': u'\U0001F4C8'},
                    {'command': '/lm', 'desc': '商品及貴金屬', 'icon': u'\U0001F4C8'},
                    {'command': '/lfx', 'desc': '外匯指數', 'icon': u'\U0001F4C8'},
                    {'command': '/lop', 'desc': '期權報告', 'icon': u'\U0001F4C8'},
                    {'command': '/lmr', 'desc': 'IB孖展', 'icon': u'\U0001F4C8'},
                    {'command': '/letf', 'desc': 'ETF表現', 'icon': u'\U0001F4C8'},
        ]

        for menuitem in menuitemlist:
            passage = passage + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc'] + ' ' + menuitem['icon']

        sHTML(update, context, passage)
    
    elif (cmd == "/lhk"):    
        randomIcon(update, context)
        sHTML(update, context, indices.get_indices("hk"))
    
    elif (cmd == "/lcn"):
        randomIcon(update, context)
        sHTML(update, context, indices.get_indices("cn"))
        
    elif (cmd == "/lw"):
        randomIcon(update, context)
        sHTML(update, context, worldindices.get_indices())
        
    elif (cmd == "/lfx"):    
        randomIcon(update, context)
        sHTML(update, context, live_rate.get_full_live_rate())
        
    elif (cmd == "/ladr"):
        randomIcon(update, context)
        sHTML(update, context, hkadr.get_hkadr())
    
    elif (cmd == "/lm"):
        randomIcon(update, context)
        sHTML(update, context, commodities.get_commodities())
        
    elif (cmd == "/letf"):
        randomIcon(update, context)
        for passage in etf_info.get_top_etf_holdings():
            sHTML(update, context, passage)
    
    elif (cmd == "/lmr"):
        pass
        url = 'https://www.interactivebrokers.com/en/index.php?f=26662&hm=hk&ex=hk&rgt=0&rsk=1&pm=0&rst=040404040401'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find("div", {"id": "hkfe"}).find("table")
        for row in table.find("tbody").find_all("tr"):
            cols = row.find_all("td")
            if cols[3].text.strip() in ('HSI', 'MHI', 'HHI'):
                msg = '%s - Intraday Init [$%s]' % (cols[3].text.strip(), cols[4].text.strip())
                sHTML(update, context, msg)

    elif (cmd == "/lop"):

        d = datetime.datetime.today()
        
        if (d.weekday() < 5):
        
            cdate = ""
            
            if (datetime.now().hour > 20):
                cdate = datetime.strftime(datetime.now(), "%y%m%d")
            else:
                today = datetime.now().date()
                yesterday = today - timedelta(days=1)
                cdate = datetime.strftime(yesterday, "%y%m%d")
           
            iurl = 'https://www.hkex.com.hk/chi/stat/dmstat/dayrpt/dqec%s.htm' % cdate
            message = "<a href='%s'>每日市場報告</a>" % iurl + EL
            message = message + "<a href='https://www.bsgroup.com.hk/futureoption/futureoption/stockoptionslist/'>可供買賣名單</a>"
            sHTML(update, context, message)
   
        else:
            brokenIcon(update, context, "Not available on weekend")
        
    elif (cmd == "/ll"):
        msg = "<a href='http://eggyolk.tech/heatmap.html' target='_blank'>Chicken Heatmap (HK)</a>" + DEL
        #msg = msg + "<a href='http://eggyolk.tech/heatmap_us.html' target='_blank'>Chicken Heatmap (US)</a>" + DEL
        msg = msg + "<a href='http://eggyolk.tech/y8.html' target='_blank'>Y8 List (HK)</a>" + DEL
        #msg = msg + "<a href='http://eggyolk.tech/y8_us.html' target='_blank'>Y8 List (US)</a>" + DEL
        msg = msg + "<a href='http://eggyolk.tech/moneyflow.html' target='_blank'>Southbound Moneyflow Track</a>" + DEL
        msg = msg + "<a href='http://eggyolk.tech/f.html' target='_blank'>Finviz Charts</a>" + DEL
        #msg = msg + "<a href='http://eggyolk.tech/y.html' target='_blank'>Y8 Charts</a>" + DEL

        sHTML(update, context, msg)
        
    else:
        unknown(update, context)   
        
def quickquote(update, context):

    menu = '<b>Quick Quote Command</b> ' + u'\U0001F4C8' + EL
    
    menuitemlist = [
                {'command': '/qM[code] [option]', 'desc': 'Monthly Chart', 'icon': u'\U0001F4C8'},
                {'command': '/qw[code] [option]', 'desc': 'Weekly Chart', 'icon': u'\U0001F4C8'},
                {'command': '/qd[code] [option]', 'desc': 'Daily Chart', 'icon': u'\U0001F4C8'},
                {'command': '/qh[code] [option]', 'desc': 'Hourly Chart', 'icon': u'\U0001F4C8'},
                {'command': '/qm[code] [option]', 'desc': 'Minutes Chart', 'icon': u'\U0001F4C8'},
                {'command': '/qa[us_code]', 'desc': 'Seeking Alpha (US only)', 'icon': u'\U0001F414'},    
                #{'command': '/qA[us_code]', 'desc': 'Motley Fool (US only)', 'icon': u'\U0001F414'},   
                #{'command': '/qb[ticker]', 'desc': 'bondsupermart Search', 'icon': u'\U0001F414'},   
                #{'command': '/qB[ticker]', 'desc': 'XTBs List (US only)', 'icon': u'\U0001F414'},   
                {'command': '/qC[code]', 'desc': 'CCASS Top 10 Distribution', 'icon': u'\U0001F42E'},
                #{'command': '/qc', 'desc': 'CBBC Distribution', 'icon': u'\U0001F42E'},
                {'command': '/qe[code]', 'desc': 'Southbound Moneyflow Trend', 'icon': u'\U0001F42E'},            
                {'command': '/qf [next] [hscei] [night]', 'desc': 'Quote HSI Mini Futures', 'icon': u'\U0001F414'},
                {'command': '/qF [next] [hscei] [night]', 'desc': 'Quote HSI Futures', 'icon': u'\U0001F414'},                   
                #{'command': '/qj[jp_code]', 'desc': 'Tokyo Stock Quote', 'icon': u'\U0001F414'}, 
                #{'command': '/ql[code]', 'desc': 'Return Charts for all Timeframes', 'icon': u'\U0001F4C8'},                    
                #{'command': '/qN[code]', 'desc': 'Result Calendar', 'icon': u'\U0001F4C8'},                    
                {'command': '/qn[code]', 'desc': 'Latest News (HK Only)', 'icon': u'\U0001F4C8'},                    
                {'command': '/qp[code]', 'desc': 'Dividend & OCF History', 'icon': u'\U0001F42E'},
                {'command': '/qq[code]', 'desc': 'Quick Quote', 'icon': u'\U0001F42E'},
                {'command': '/qr[code1] [code2]', 'desc': 'Relative Strength', 'icon': u'\U0001F42E'},
                #{'command': '/qR', 'desc': 'Industries List', 'icon': u'\U0001F42E'},
                {'command': '/qs', 'desc': 'Chicken Sectormap', 'icon': u'\U0001F414'},
                {'command': '/qS[code]', 'desc': 'Get Company Profile', 'icon': u'\U0001F414'},
                #{'command': '/qt[searchkey]', 'desc': 'Get 28hse Price History', 'icon': u'\U0001F414'},
                {'command': '/qv[code]', 'desc': 'Finviz qChart (US only)', 'icon': u'\U0001F414'}, 
                {'command': '/qY', 'desc': 'Treasury Yield', 'icon': u'\U0001F414'}, 
    ]
    
    fxc = ", ".join(['/qh' + str(x.name) for x in FxCode][:3])
    idxc = ", ".join(['/qd' + str(x.name) for x in IndexCode][:3])

    for menuitem in menuitemlist:
        menu = menu + EL + ' ' + menuitem['command'] + ' - ' + menuitem['desc']
    
    menu = menu + DEL + "[option]: bb - 保力加, sma/gcc - SMAs, night - 夜期"
    
    menu = menu + DEL + "<b>Sample</b>"
    menu = menu + EL + "Stock: /qd5, /qm601318, /qMAAPL, /qwMCD"   
    menu = menu + EL + "FX: " + fxc
    menu = menu + EL + "Index: " + idxc  
    menu = menu + EL + "News / CCASS: /qn5, /qn3333, /qC606"     
    menu = menu + EL + "Profile (HK): /qS5, /qS981"     
    menu = menu + EL + "Southbound Moneyflow: /qe5, /qe581"     
    menu = menu + EL + "Rel Strength: /qr5 2388 3988"        

    sHTML(update, context, menu)

def quickquoteHandler(update, context):

    logger.info("QQ Command received: [%s]" % (update.message.text))
    
    commands = update.message.text
    commands = commands.split("@")[0] #remove bot suffix
    chat_id = update.effective_chat.id
    
    if (commands.startswith("/q")):
    
        action = commands[2]
        parameters = []
        code =  None
    
        # commands check
        if commands[3:]:            
            parameters = commands[3:].split()
            code = parameters[0]      
        
        logger.info("QQ Actions/Params received: [%s > %s]" % (action, str(parameters)))
            
        if (action in ["M", "w", "d", "h", "m"]):
        
            # Bucket Scenario to display stock chart
            if parameters:
            
                if(is_white_listed(chat_id)):
                
                    logger.info("White Listed: [" + str(chat_id) + "]")      
                    randomIcon(update, context)                    
                    linklist = charting.get_hkg_chart_list_by_action(action, parameters)
                    
                    for link_dict in linklist:
                        try:
                            f = urllib.request.urlopen(link_dict['url'], timeout=10)                            
                        except:
                            traceback.print_exc()
                            logger.info("URL: %s" % link_dict['url'])
                            if 'finviz' in link_dict['url']:
                                sHTML(update, context, u'\U0001F423 ' + ('<a href="%s">%s</a>' % (link_dict['url'], link_dict['code'])))
                            else:
                                sHTML(update, context, u'\U000026D4' + ' Request Timeout for [' + link_dict['code'] + ']')
                        else:
                            sIMAGE(update, context, f)
                else:
                    logger.info("Not in White List: [" + str(chat_id) + "]")
                    sHTML(update, context, u'\U000026D4' + ' Request Timeout')
            
            # no parameters case
            else:
                stockcode = random.choice(["2628", "939", "2800", "8141", "AAPL", "GOOG", "GS"])
                p1 = "<i>Usage:</i> " + commands + "[StockCode] (e.g. /q" + action + stockcode + ")"

                p2 = "<i>Sample (Futures):</i>" + EL
                for fCode in fcharting.DICT_FINVIZ_FUTURES:
                    p2 = p2 + commands + fCode + " - " + fcharting.DICT_FINVIZ_FUTURES[fCode][1] + EL

                p3 = "<i>Sample (Crypto):</i>" + EL
                for fCode in fcharting.DICT_FINVIZ_CRYPTO:
                    p3 = p3 +commands + fCode + " - " + fcharting.DICT_FINVIZ_CRYPTO[fCode][1] + EL

                passage = random.choice([p1, p2, p3])
                sHTML(update, context, passage)        
                return
        
        elif (action == "a"):
        
            if not parameters:
                sTEXT(update, context, "Sample: /qa[US_StockCode]")
            elif (is_number(code)):
                sTEXT(update, context, "Only US Stock is supported")
            else:
                rhtml = analysis_loader.get_analysis(code)
                sHTML(update, context, rhtml)
            return
        
        elif (action == "C"):

            if not parameters:
                sTEXT(update, context, "Sample: /qC[HK_StockCode]")
            else:        
                randomIcon(update, context)        
                sHTML(update, context, ccass_loader.get_latest_ccass_info(code, 20))
                sHTML(update, context, ccass_loader.get_shareholding_disclosure(code))
                return       

        elif (action == "e"):            

            if not parameters:
                sTEXT(update, context, "Sample: /qe[HK_StockCode]")      
                return

            randomIcon(update, context)     
            for stockCd in parameters:
                sHTML(update, context, mutual_market.get_moneyflow_by_code(stockCd))
            return            
            
        elif (action == "f"):
            sHTML(update, context, futures.get_futures("M", parameters))
            return

        elif (action == "F"):
            sHTML(update, context, futures.get_futures("N", parameters))
            return

        elif (action == "H"):
        
            if not parameters:
                sTEXT(update, context, "Sample: /qh[US_ETFStockCode]")      
            elif (not is_number(code)):
                randomIcon(update, context)        
                sHTML(update, context, etf_info.get_etf_profile(code))
                sHTML(update, context, etf_info.get_etf_holdings(code))
            else:
                sHTML(update, context, "Only US ETFs are supported")

        elif (action == "N"):
            
            if not parameters:
                sTEXT(update, context, "Sample: /qN[HKStockCode]")    
            elif (is_number(code)):
                sHTML(update, context, result_announcement.get_result_calendar(code))
            else:
                path = usearning.gen_earning_chart(code)
                if path:
                    sHTML(update, context, u'\U0001F333' + ' ' + ("Earning History for %s" % code))
                    sIMAGE(update, context, open(path, 'rb'))
                else:
                    sHTML(update, context, u'\U000026D4' + ' No History found for [' + code + ']')

        elif (action == "n"):

            if not parameters:
                sTEXT(update, context, "Sample: /qn[StockCode]")    
            elif (is_number(code)):
                sHTML(update, context, company_news.get_latest_news_by_code(code, 8))
            else:
                sHTML(update, context, us_company_news.get_latest_news_by_code(code, 10))
            return    
                        
        elif (action == "p"):
        
            if not parameters:
                sTEXT(update, context, "Sample: /qh[HK_StockCode]")    
            elif (is_number(code)):
                sHTML(update, context, company_profile.get_dividend(code))
                sHTML(update, context, company_profile.get_cashflow(code))
            else:
                bot.sendMessage(chat_id, "Only HK Stock is supported", parse_mode='HTML')
            return    
 
        elif (action.lower() == "q"):

            # Get quick quote from AAStocks
            simpleMode = True
            if (action == "Q"):
                simpleMode = False
                
            if not parameters:
                sTEXT(update, context, "Sample: /qq[StockCode]")      
                return
            
            for stockCd in parameters:
                if (stockCd.strip().isdigit() and len(stockCd.strip()) == 6):
                    sHTML(update, context, stock_quote.get_quote_message(stockCd, "CN", simpleMode))
                elif (stockCd.strip().isdigit()):
                    sHTML(update, context, stock_quote.get_quote_message(stockCd, "HK", simpleMode))
                elif (stockCd.strip()):

                    if (stockCd.upper() in CRYPTO_CURRENCY):
                        sHTML(update, context, crypto_quote.get_crypto_quote_message(stockCd.upper()))
       
                    elif (stockCd.upper() in DICT_CURRENCY):
                        fromCur = DICT_CURRENCY[stockCd.upper()][0:3]
                        toCur = DICT_CURRENCY[stockCd.upper()][3:6]
                        sHTML(update, context, fx_quote.get_fx_quote_message(fromCur, toCur))

                    else:
                        sHTML(update, context, iex_stock_quote.get_quote_message(stockCd, "US", simpleMode))
        
        elif (action == "r"):
        
            if not parameters:
                sTEXT(update, context, "Sample: /qr[StockCode1] [StockCode2]...")      
                return
            
            sHTML(update, context, random.choice(LOADING))         
            try:
                logger.info(str(parameters))
                result = stock_history.get_stocks_rs_charts(parameters)
                chartpath = result[0]
                invalidcodelist = result[1]
                logger.info("Chart Path: [" + chartpath + "]")

            except Exception as e:
                logger.info("Exception raised: [" + str(e) +  "]")
                sHTML(update, context, u'\U000026D4' + ' ' + str(e))
            else:
                if(len(invalidcodelist) > 0):
                    sHTML(update, context, u'\U000026D4' + " Stocks with no data: " + str(invalidcodelist))
                
                sIMAGE(update, context, open(chartpath, 'rb'))
                
            return
            
        elif (action == "S"):
        
            if not parameters:
                sTEXT(update, context, "Sample: /qS[HKStockCode]")      
                return
                
            passage = company_profile.get_profile(code)
            results = [passage[i:i+MAX_MSG_SIZE] for i in range(0, len(passage), MAX_MSG_SIZE)]

            for result in results:
                sHTML(update, context, result)
                
        elif (action == "s"):

            sHTML(update, context, u'\U0001F414' +  u'\U0001F413' + u'\U0001F4B9')
            
            try:
                f = urllib.request.urlopen("http://www.fafaworld.com/usectors.jpg", timeout=10)
                f2 = urllib.request.urlopen("http://www.fafaworld.com/usectorsus.jpg", timeout=10)
            except:
                sHTML(update, context, u'\U0001F423' + ' Request Timeout')
            else:
                sIMAGE(update, context, f)
                sIMAGE(update, context, f2)            
            return                 
        
        elif (action == "v"):

            if not parameters:
                sTEXT(update, context, "Sample: /qv[USStockCode1] [USStockCode2]...")      
                return
        
            urls = heatmap.get_charts(code, parameters[1:])

            for url in urls:
                cdd = url.split('?')[1].split('&')[0].split('=')[1]
                sHTML(update, context, u'\U0001F423 ' + ('<a href="%s">%s</a>' % (url, cdd)))

            return
        
        elif (action == "V"):

            if not parameters:
                sTEXT(update, context, "Sample: /qV[USStockCode1] [USStockCode2]...")      
                return

            urls = scharting.get_charts(code, parameters[1:])

            for url in urls:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                    remote_image = requests.get(url, headers=headers)
                    f = io.BytesIO(remote_image.content)
                except:
                    traceback.print_exc()
                    sHTML(update, context, u'\U0001F423' + ' Request Timeout')
                else:
                    sIMAGE(update, context, f)
            return
    
        elif (action == "Y"):
            result = ust.get_ust_yield()
            
            if (result):
                sHTML(update, context, result[0])

                try:
                    f = urllib.request.urlopen(result[1], timeout=10)
                except:
                    pass
                else:
                    sIMAGE(update, context, f)
            else:
                sHTML(update, context, u'\U0001F423' + ' Request Error')       
        
        else:
            unknown(update, context)  
    else:
        unknown(update, context)            
    
def commandHandler(update, context):

    logger.info("Command from %s: [%s]" % (update.effective_chat.id, update.message.text))
    
    commands = update.message.text
    
    if (commands.startswith("/lib")):

        parameters = commands.strip("/lib")
        logger.info("Parameters from %s: [%s]" % (update.effective_chat.id, parameters))  

        try:
            [p1, p2] = parameters.split()
            ibcard_dict = dict(config.items('ibcard'))
            result = ("%s %s" % (ibcard_dict.get(p1), ibcard_dict.get(p2)))
            sTEXT(update, context, result)
        except:
            traceback.print_exc()
            unknown(update, context)  
        
    elif (commands.startswith("/q")):    
    
        # bucket handler for quick quote commands
        quickquoteHandler(update, context)
        
    else:
        unknown(update, context)          
        

        
################### updater setup
TOKEN = config.get("telegram","bot-id") # get token from command-line
updater = Updater(token=TOKEN, use_context=True)

################### handler setup
handler_list = [

    CommandHandler('cal', cal),    

    CommandHandler('l', livequote),  
    CommandHandler('ladr', livequote),
    CommandHandler('lhk', livequote),
    CommandHandler('lcn', livequote),
    CommandHandler('lw', livequote),
    CommandHandler('lm', livequote),
    CommandHandler('lfx', livequote),  
    CommandHandler('lop', livequote),
    CommandHandler('lmr', livequote),
    CommandHandler('letf', livequote),
    CommandHandler('ll', livequote),
    
    CommandHandler('q', quickquote),  

    CommandHandler('start', start),
    CommandHandler('test', test),
    CommandHandler('top10', top10),
    CommandHandler('ttETF', top10),
    CommandHandler('ttBanks', top10),
    CommandHandler('ttREIT', top10),
    CommandHandler('ttCong', top10),  

    # Bucket handler for
    # /lib
    # /q*
    MessageHandler(Filters.command, commandHandler),
    
    MessageHandler(Filters.text & (~Filters.command), textLog),
]

################### dispatcher setup
dispatcher = updater.dispatcher

for handler in handler_list:
    dispatcher.add_handler(handler)

################### Main Program
try:
    updater.start_polling()
except Exception as e:
    logger.critical(e, exc_info=True)
