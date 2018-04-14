#! /usr/bin/python

import pandas as pd
import datetime
from datetime import tzinfo, timedelta, datetime
import time
import os

import traceback
import logging
import sys

import redis

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)

def getV(variable_name):
    my_server = redis.Redis(connection_pool=POOL)
    response = my_server.get(variable_name)
    return response

def setV(variable_name, variable_value):
    my_server = redis.Redis(connection_pool=POOL)
    my_server.set(variable_name, variable_value)

def main():

    print("main....")
    end = datetime.today()
    start = end - timedelta(days=(1*365))
    
    #setV("Winston", "test")
    print(getV("Winston"))

if __name__ == "__main__":
    main()

