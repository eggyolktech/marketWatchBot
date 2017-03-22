from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request
import urllib.parse
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

def get_fx_live_rate(quote):

    url = config.get("fxcm","rates-xml")
   
    r = requests.get(url)
    xml = r.text
    soup = BeautifulSoup(xml, 'xml')

    #<Rate Symbol="EURUSD">
    #<Bid>1.05896</Bid>
    #<Ask>1.06001</Ask>
    #<High>1.06287</High>
    #<Low>1.05372</Low>
    #<Direction>0</Direction>
    #<Last>16:57:55</Last>
    #</Rate>
    # look in the main node for object's with attr=name, optionally look up attrs with regex
    
    rate = soup.find('Rate', {'Symbol': quote})
    live_rate = ''
    
    if(rate):
        
        direction = u'\U000027A1'
        
        if (int(rate.find('Direction').text) > 0):
            direction = u'\U00002B06'
        elif (int(rate.find('Direction').text) < 0):
            direction = u'\U00002B07'

        return "Bid: " + rate.find('Bid').text + " / Ask: " + rate.find('Ask').text + " " + direction
    else:
        return "No live rate is returned."

def get_dxy_live_rate():

    url = config.get("wsj","dxy-url")
   
    r = requests.get(url)
    html = r.text
    #print(html.encode("utf-8"))
    soup = BeautifulSoup(html, "html5lib")
    
    last = soup.find('span', {"id" : "quote_val"}).text
    change = soup.find('span', {"id" : "quote_changePer"}).text

    if last:
        
        if (not change.startswith("-")):
            direction = u'\U00002B06'
        else:
            direction = u'\U00002B07'

        return "Last: " + last + " / Change: " + change + " " + direction
    else:
        return "No live rate is returned."
        
        
def main():

    print(get_fx_live_rate("EURUSD").encode("utf-8"))
    
    print(get_dxy_live_rate().encode("utf-8"))

if __name__ == "__main__":
    main()    
        

