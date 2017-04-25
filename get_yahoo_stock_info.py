import pandas as pd
import pandas_datareader.data as web  # Package and modules for importing data; this code may change depending on pandas version
import time
import datetime
import configparser
import matplotlib.pyplot as plt   # Import matplotlib
import json

from classes.AastocksConstants import *

config = configparser.ConfigParser()
config.read('config.properties')

def get_stocks_rs_industry_list():

    passage = "List Relative Strength by Industries" + DEL

    with open('data/list_TopIndustryList.json', encoding="utf-8") as data_file:    
        indexlists = json.load(data_file)    
        
    for indexlist in indexlists:
        code = indexlist["code"]
        passage = passage + "/qR" + code + " (" + indexlist["label"] + ")" + EL  
        
    return passage  
    
def get_stocks_rs_list(code, limit):

    result = []
    codelist = []
    
    with open('data/list_TopIndustryList.json', encoding="utf-8") as data_file:    
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

def get_stocks_rs_charts(codelist):

    DEL = "\n\n"
    EL = "\n"
    chartpath = ""
    codelist = codelist[:10]
    
    # We will look at stock prices over the past year, starting at April 1, 2016
    start = datetime.datetime(2016,4,1)
    end = datetime.date.today()

    #for code in codelist:
    #    if (not is_number(code)):
    #        raise ValueError("Non-numeric code found: [" + code + "]\n<i>Usage:</i> " + "/qr" + "[code1] [code2] [code3].... (e.g. " + "/qr2800 2822 2823" + ")")    

    startdatelist = []  
    stockcodelist = []
    codedflist = []
    invalidcodelist = []
    result = []    
            
    for code in codelist:
        
        if (code[0] == "0"):
            code = code[1:]
        
        if (is_number(code)):
            code = code.rjust(4, '0') + ".HK"
        else:
            code = code.upper()            
            if (code in ['HSI', 'HSCE', 'HSCC',  'HSNF',  'HSNC',  'HSNU', 'HSNP']):
                code = "^" + code
        
        try:
            codedf = web.DataReader(code, "yahoo", start, end)
            if (not '^' in code or code == "^HSI"):
                codedf = codedf[codedf.Volume != 0]
                
            print("Retrieved Data from Yahoo for code: [" + code + "]")
            
            stockcodelist.append(code)
            codedflist.append(codedf)
            startdatelist.append(codedf.index[0])

        except Exception as e:
            print("Exception raised: [" + str(e) +  "]")
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

    print(stocks.head())
    print(stocks.tail())
    
    stocks_return = stocks.apply(lambda x: x / x[0])    

    plt.style.use('ggplot')
    
    stocks_return.plot(figsize=(10,6), grid = True, linewidth=1.0, title="Relative Strength since 2016 Apr", colormap = plt.cm.rainbow).axhline(y = 1, color = "black", lw = 1) 
    plt.legend(loc='upper left')
    
    chartpath = "C:\\Temp\\" + 'ychart' + str(int(round(time.time() * 1000))) + '.png'
    
    #print(chartpath)
    
    plt.savefig(chartpath, bbox_inches='tight')
    #plt.show()
    
    result.append(chartpath)
    result.append(invalidcodelist)
    return result
    
   
def main():

    try:
        print(get_stocks_rs_charts("494 293".split()))
        #print(get_stocks_rs_charts("5 2388111".split()))
        print(get_stocks_rs_charts("2388".split()))
        print(get_stocks_rs_charts("66 2388".split()))
        print(get_stocks_rs_charts(["66", "2828", "2800"]))
        
    except ValueError as ve:
        print("Value Error: [" + str(ve) + "]")
    except Exception as e:
        print("Exception: [" + str(e) + "]")
    
    
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()                
              



