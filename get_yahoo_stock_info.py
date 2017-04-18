import pandas as pd
import pandas_datareader.data as web  # Package and modules for importing data; this code may change depending on pandas version
import time
import datetime
import configparser
import matplotlib.pyplot as plt   # Import matplotlib


config = configparser.ConfigParser()
config.read('config.properties')

def get_stocks_rs_charts(codelist):

    DEL = "\n\n"
    EL = "\n"
    chartpath = ""
    codelist = codelist[:10]
    
    # We will look at stock prices over the past year, starting at April 1, 2016
    start = datetime.datetime(2016,4,1)
    end = datetime.date.today()

    for code in codelist:
        if (not is_number(code)):
            raise ValueError("Non-numeric code found: [" + code + "]<br><i>Usage:</i> " + "/qr" + "[code1] [code2] [code3].... (e.g. " + "/qr2800 2822 2823" + ")")    

    startdatelist = []  
    stockcodelist = []
    codedflist = []    
            
    for code in codelist:
        code = code.rjust(4, '0') + ".HK"
        codedf = web.DataReader(code, "yahoo", start, end)
        print("Retrieved Data from Yahoo for code: [" + code + "]")
        
        stockcodelist.append(code)
        codedflist.append(codedf)
        startdatelist.append(codedf.index[0])
        
    maxstartdate = max(startdatelist)
    
    codedfloclist = []
    
    for codedf in codedflist:
        codedf = codedf.loc[maxstartdate:]
        codedfloclist.append(codedf)    
    
    # form the df dict
    codedic = {}
    
    for idx, codeval in enumerate(stockcodelist):
        codedic[codeval] = codedfloclist[idx]["Adj Close"]
    
    stocks = pd.DataFrame(codedic)

    print(stocks.head())
    
    stocks_return = stocks.apply(lambda x: x / x[0])    
    
    plt.style.use('ggplot')
    
    stocks_return.plot(figsize=(10,6), grid = True, linewidth=1.0, title="Relative Strength since 2016 Apr").axhline(y = 1, color = "black", lw = 1) 
    plt.legend(loc='upper left')
    
    chartpath = "C:\\Temp\\" + 'ychart' + str(int(round(time.time() * 1000))) + '.png'
    
    plt.savefig(chartpath, bbox_inches='tight')
    #plt.show()
    
    return chartpath   
   
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
              



