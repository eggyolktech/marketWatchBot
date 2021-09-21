#!/usr/bin/python3.6

from flask import Flask, request, jsonify

import datetime
import json
import easyquotation

app = Flask(__name__)

quotation = easyquotation.use("hkquote")

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Hello World!"

@app.route('/quote', methods=['GET', 'POST'])
def quote():

    code = request.args.get('code')
    #data = quotation.real(['00001','15541'])
    data = quotation.real([code.zfill(5)])

    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

