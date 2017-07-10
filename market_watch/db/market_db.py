#!/usr/bin/python
import sqlite3

DB_FILE = '/app/marketWatchBot/market_watch/db/market_db.dat'

def init():

    conn = sqlite3.connect(DB_FILE)

    print("Opened database successfully")
    
    conn.execute('DROP TABLE IF EXISTS PROFIT_WARNING;')
    
    conn.execute('''CREATE TABLE PROFIT_WARNING 
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       LOG_TIME           TEXT    NOT NULL,
       LOG_TYPE                 CHAR(2));''')

    print("Table created successfully")

    conn.close()

def list_warning():
    
    conn = sqlite3.connect(DB_FILE)

    for row in conn.execute("SELECT * FROM PROFIT_WARNING ORDER BY LOG_TIME ASC"):
        print(row)

    conn.close()


def add_warning(logtime, logtype):

    conn = sqlite3.connect(DB_FILE)

    t = (logtime, logtype)
    cursor = conn.execute('SELECT * FROM PROFIT_WARNING WHERE LOG_TIME=? AND LOG_TYPE=?', t)
    
    # There is record already
    if (cursor.fetchone()):
        conn.close()
        return False
    # Blank new case
    else:
        conn.execute("INSERT INTO PROFIT_WARNING (LOG_TIME, LOG_TYPE) VALUES (?, ?)", t)
        conn.commit()
        conn.close()
        return True

def main():

    #init()
    #print(add_warning('04/07/2017 18:33','+'))
    #print(add_warning('04/07/2017 18:33','+'))
    #print(add_warning('04/07/2017 19:32','-'))
    #print(add_warning('04/07/2017 19:32','-'))
    list_warning()    
   
if __name__ == "__main__":
    main()        
        

