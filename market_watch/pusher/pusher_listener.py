#!/usr/bin/python

import datetime
import json
import sys
import pysher
import time

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

appkey = '7df7c4eefab95722ea49'

#  def __init__(self, key, cluster="", secure=True, secret="", user_data=None, log_level=logging.INFO,
#                 daemon=True, port=443, reconnect_interval=10, custom_host="", auto_sub=False,
#                 http_proxy_host="", http_proxy_port=0, http_no_proxy=None, http_proxy_auth=None,
#                 **thread_kwargs):

pusher = pysher.Pusher(key=appkey, cluster='ap1', secret='9cdfb62c24360d4e45ab')

def  my_func(*args, **kwargs):
    print("processing Args:", args)
    print("processing Kwargs:", kwargs)

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher.subscribe('mychannel')
    channel.bind('myevent', my_func)

pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
    # Do other things in the meantime here...
    time.sleep(1)


