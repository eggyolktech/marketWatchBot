#!/usr/bin/python

import datetime
import pusher
import json

import pusher

pusher_client = pusher.Pusher(
  app_id='1269376',
  key='7df7c4eefab95722ea49',
  secret='9cdfb62c24360d4e45ab',
  cluster='ap1',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

