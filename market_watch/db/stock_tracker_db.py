#!/usr/bin/python
import sqlite3

DB_FILE = '/app/marketWatchBot/market_watch/db/market_db.dat'

def init():

    conn = sqlite3.connect(DB_FILE)

    print("Opened database successfully")
    
    conn.execute('DROP TABLE IF EXISTS STOCK_TRACKER;')
    
    conn.execute('''CREATE TABLE STOCK_TRACKER 
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       LOG_PERIOD         VARCHART(2)   NOT NULL,
       LOG_CODE           TEXT    NOT NULL,
       LOG_DATE           TEXT    NOT NULL,
       LOG_PRICE          DECIMAL(10,2) NOT NULL, 
       LOG_DESC           TEXT    NOT NULL,
       REGION             VARCHAR(2) NOT NULL);''')

    print("Table created successfully")

    conn.close()

def list_tracker():
    
    conn = sqlite3.connect(DB_FILE)

    for row in conn.execute("SELECT * FROM STOCK_TRACKER ORDER BY LOG_DATE ASC"):
        print(row)

    conn.close()


def add_tracker(logdate, logcode, logprice, logperiod, logdesc, region):

    conn = sqlite3.connect(DB_FILE)

    t = (logcode, logdate, logperiod)
    cursor = conn.execute('SELECT * FROM STOCK_TRACKER WHERE LOG_CODE=? AND LOG_DATE=? AND LOG_PERIOD=?', t)
    
    # There is record already
    if (cursor.fetchone()):
        conn.close()
        return False
    # Blank new case
    else:
        t = (logdate, logcode, logprice, logperiod, logdesc, region) 
        conn.execute("INSERT INTO STOCK_TRACKER (LOG_DATE, LOG_CODE, LOG_PRICE, LOG_PERIOD, LOG_DESC, REGION) VALUES (?, ?, ?, ?, ?, ?)", t)
        conn.commit()
        conn.close()
        return True

def remove_tracker(logdate, logcode, logperiod):

    conn = sqlite3.connect(DB_FILE)

    t = (logdate, logcode, logperiod)
    conn.execute("DELETE FROM STOCK_TRACKER WHERE LOG_DATE = ? AND LOG_CODE = ? AND LOG_PERIOD = ?", t)
    conn.commit()
    conn.close()
    return True
    

def main():

    #init()
    #print(add_warning('04/07/2017 18:33','+'))
    #print(add_warning('04/07/2017 18:33','+'))
    #print(add_warning('04/07/2017 19:32','-'))
    #print(add_warning('04/07/2017 19:32','-'))
    add_tracker('20170713', '823', 60.20, 'D', 'M1, D1', 'HK')
    #add_tracker('20170713', '1', 80.20, 'D', 'M1, D1')
    #list_tracker()    
    remove_tracker('20170713', '823', 'D')
    list_tracker()
   
if __name__ == "__main__":
    main()        
        

