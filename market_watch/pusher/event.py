#!/usr/bin/python

import datetime
import pusher
import json

pusher_client = pusher.Pusher(
    app_id='671005',
    key='12a3c291576ece3e9f88',
    secret='4ea651fcca55c2afb204',
    cluster='ap1',
    ssl=True
)

message = {'title':'Hello World', 'content':'TestTestTest','created': str(datetime.datetime.now())}

pusher_client.trigger('my-channel', 'my-event', message)

