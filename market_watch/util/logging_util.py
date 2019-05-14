#!/usr/bin/python

import logging
import os

def get_logger(filename):

    filename = filename.split("/")[1]
    filename = filename.split(".")[0]
    logpath = '/app/marketWatchBot/market_watch/log/%s.log' % filename    

    lformat = '%(asctime)s %(levelname)s:%(message)s'
    datefmt = '%m/%d/%Y %I:%M:%S %p'

    logging.basicConfig(filename=logpath, format=lformat, datefmt=datefmt, level=logging.DEBUG)
    return logging
    
def main():
    print(os.path.splitext(os.path.realpath(__file__))[0])

if __name__ == "__main__":
    main() 
