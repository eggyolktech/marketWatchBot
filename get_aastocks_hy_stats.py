# imdb process import
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import re
from datetime import date
from datetime import datetime
import configparser
#config = ConfigParser.RawConfigParser()
#config.read('ConfigFile.properties')


def get_aastocks_etf_stat():

    passage = ""

    url = "http://www.aastocks.com/en/stocks/etf/search.aspx?t=5&s=421&o=0&y=3"
    
    #http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx?industrysymbol=5011&t=1&hk=0&s=10&o=0
    #http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx?industrysymbol=6013&t=1&s=10&o=0&p=
    
    print("Url: [" + url + "]")
    
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    table = soup.find('table', id="tabETF1")
    tbody = table.find('tbody')
    rows = tbody.findAll('tr')
    
    count = 0
    
    # skip the skewed records
    for row in rows[1:]:
    
        if (count == 10):
            break
            
        count = count + 1
                
        _etfname = row.select('td')[0].text
        _etfcode = row.select('td')[1].text
        
        _dps = row.select('td')[2].text
        _latesty = row.select('td')[3].text
        _last1yry = row.select('td')[4].text
        _last2yry = row.select('td')[5].text
        _last3yry = row.select('td')[6].text
        _3yravgy = row.select('td')[7].text
        _policy = str(row.select('td')[8].text)
        _policy = re.sub(r'[^\x00-\x7F]+','', _policy)
        
        passage = passage + "<b>" + str(count) + ". " + _etfname + " (" + _etfcode + ")" + "</b>" + "\n" + "DPS " + _dps + " <i>@" + _latesty + "</i> " + _policy + "\n\n"
        
        
        #print(passage)
    
   #<tr> <td valign="middle" class="col1" style="padding-left: 2px;"> <a href="/en/stocks/quote/detail-quote.aspx?symbol=02818" class="a8 cls etfDLSName" title="ETF - Ping An of China CSI RAFI A-Share 50 ETF">Ping An of China CSI RAFI A-Share 50 ETF</a> </td> <td valign="middle" class="col2"><a href="http://www.aastocks.com/en/ltp/rtquote.aspx?symbol=02818" class="a14 cls" title="02818">02818.HK</a></td> <td valign="middle" class="col3 cls"><span class="greya">HKD</span> 15.070</td> <td valign="middle" class="col4 cls"><b>90.89%</b></td> <td valign="middle" class="col5 cls">N/A</td> <td valign="middle" class="col6 cls">N/A</td> <td valign="middle" class="col7 cls">N/A</td> <td valign="middle" class="col8 cls">N/A</td> <td valign="middle" class="col9">&nbsp;Annual</td> <td valign="middle" class="col10"><a href="/en/stocks/analysis/dividend.aspx?symbol=02818" class="lnk">View&nbsp;&gt;&gt;</a></td> <td class="col11" style="padding-right: 2px;"><input type="checkbox" onclick="AddComp('02818', 'Ping An of China CSI RAFI A-Share 50 ETF', this)"></td> </tr> 

    if (passage == ""):
        passage = "No event for today."
    else:
        passage = "<b>Top 10 ETFs with highest Divdends</b>\n\n" + passage
    
    
    print("Passage: [" + passage + "]")
    return passage
    
 
def send_to_tg_chatroom(passage): 

    bot_id = "193192163:AAGC4RFnLmU7uJSbrJFPz1y36202O_NJcDU"
    result = urllib.request.urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": -172861420, "text": passage }).encode("utf-8")).read()
    print(result) 
    
    #result = urllib.request.urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": -1001091025553, "text": passage }).encode("utf-8")).read()
    #print(result) 
  
# sync top 100 list
passage = get_aastocks_etf_stat()

print(passage)

# Send a message to a chat room (chat room ID retrieved from getUpdates)
send_to_tg_chatroom(passage)
