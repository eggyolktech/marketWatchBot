import pandas as pd
import pandas_datareader.data as web  # Package and modules for importing data; this code may change depending on pandas version
import time
import datetime
import configparser
import matplotlib.pyplot as plt   # Import matplotlib


config = configparser.ConfigParser()
config.read('config.properties')

def get_stocks_rs_charts(code1, code2):

    DEL = "\n\n"
    EL = "\n"
    chartpath = ""

    if (is_number(code1) and is_number(code2)):
        print("Codes to Compare: [" + code1 + ", " + code2 + "]")
    else:
        raise ValueError("<i>Usage:</i> " + "/qr" + "[code1] [code2] (e.g. " + "/qr2800 2822" + ")")    
    
    # We will look at stock prices over the past year, starting at January 1, 2016
    start = datetime.datetime(2016,4,1)
    end = datetime.date.today()
 
    # Let's get Apple stock data; Apple's ticker symbol is AAPL
    # First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
    code1 = code1.rjust(4, '0') + ".HK"
    code2 = code2.rjust(4, '0') + ".HK"
    #code1 = "HSI"
    code1tf = web.DataReader(code1, "yahoo", start, end)
    code2tf = web.DataReader(code2, "yahoo", start, end)
 
    startdate1 = code1tf.index[0]
    startdate2 = code2tf.index[0]

    if (startdate1 < startdate2):        
        code1tf = code1tf.loc[startdate2:]
    elif (startdate1 > startdate2):
        code2tf = code2tf.loc[startdate1:]
    
    stocks = pd.DataFrame({code1: code1tf["Adj Close"],
                           code2: code2tf["Adj Close"]})
                           
    
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
        print(get_stocks_rs_charts("494", "293"))
        #print(get_stocks_rs_charts("5", "2388111"))
        print(get_stocks_rs_charts("5", "2388A"))
        print(get_stocks_rs_charts("66 ", "2388"))
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
              



