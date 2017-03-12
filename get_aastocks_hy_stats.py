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


def get_aastocks_etf_stat(url):

    passage = ""

    print("ETF Url: [" + url + "]")
    
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

    if (passage == ""):
        passage = "No ETFs record for today."
    else:
        passage = "<b>Top 10 ETFs with highest dividends</b>\n\n" + passage
    
    print("Passage: [" + passage + "]")
    return passage

def get_aastocks_hy_stat(url, industry):

    passage = ""
    
    print("Url: [" + url + "]")
    
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    table = soup.find('table', id="tbTS")
    tbody = table.find('tbody')
    rows = tbody.findAll('tr')
    
    count = 0
    
    # skip the skewed records
    for row in rows:
    
        if (count == 10):
            break
            
        count = count + 1
        
        _name = row.select('td')[0].select('div')[0].select('div')[0].select('span')[0].text
        _code = row.select('td')[0].select('a')[0].text
        
        _quote = row.select('td')[2].text
        _peratio = row.select('td')[7].text
        _pbratio = row.select('td')[8].text
        _yield = row.select('td')[9].text
        _marketcap = row.select('td')[10].text  

        print(_name)
        print(_code)
        
        passage = passage + "<b>" + str(count) + ". " + _name + " (" + _code + ")" + "</b>" + "\n" + "$" + _quote + " <i>@" + _yield + ", P/E(x): " + _peratio + ", P/B(x): " + _pbratio +"</i> MCP: " + _marketcap + "\n\n"

    if (passage == ""):
        passage = "No bank stock records for today."
    else:
        passage = "<b>Top 10 " + industry + " with highest dividends</b>\n\n" + passage
    
    print("Passage: [" + passage + "]")
    return passage
    
    
def send_to_tg_chatroom(passage): 

    bot_id = "193192163:AAGC4RFnLmU7uJSbrJFPz1y36202O_NJcDU"
    result = urllib.request.urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": -172861420, "text": passage }).encode("utf-8")).read()
    print(result) 
    
    #result = urllib.request.urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urllib.parse.urlencode({ "parse_mode": "HTML", "chat_id": -1001091025553, "text": passage }).encode("utf-8")).read()
    #print(result) 
  
passage = get_aastocks_etf_stat("http://www.aastocks.com/en/stocks/etf/search.aspx?t=5&s=421&o=0&y=3")

# Send a message to a chat room (chat room ID retrieved from getUpdates)
send_to_tg_chatroom(passage)

passage = get_aastocks_hy_stat("http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx?industrysymbol=5011&t=1&hk=0&s=10&o=0", "Banks")

send_to_tg_chatroom(passage)

passage = get_aastocks_hy_stat("http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx?industrysymbol=6013&t=1&s=10&o=0&p=", "REITs")

send_to_tg_chatroom(passage)

passage = get_aastocks_hy_stat("http://www.aastocks.com/en/stocks/market/industry/sector-industry-details.aspx?industrysymbol=8001&t=1&s=10&o=0&p=", "Conglomerates")

send_to_tg_chatroom(passage)

