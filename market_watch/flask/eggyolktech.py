#!/usr/bin/python

from flask import Flask, request
from pymongo import MongoClient
from market_watch.util import config_loader

import datetime
import json

app = Flask(__name__)

config = config_loader.load()
conn_str = config.get("mongodb", "connection")

client = MongoClient(conn_str)
db = client.test

@app.route('/', methods=['GET', 'POST'])
def contact():
    
    name = request.form.get('yourname')
    mail = request.form.get('email')
    message = request.form.get('yourmessage')

    if name and message:
        post = {}
        post['author'] = name
        post['email'] = mail
        post['message'] = message
        post['date'] = datetime.datetime.now()
        db.posts.insert(post)    

    return ("<h3 style='color:blue'>Thanks for your message %s!</h3>" % name)

@app.route('/list/')
def list():

    msg = ""

    for post in db.posts.find():
        msg = msg + "<li>%s</li>" % post

    msg = "<ol>%s</ol>" % msg
    return (msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

