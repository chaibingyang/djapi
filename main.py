#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: dj
@contact: dj@itmojun.com
@software: PyCharm
@file: main.py
@time: 2018/12/5 20:32
"""

import json
import urllib
import flask
from werkzeug.contrib.fixers import ProxyFix

def get_robot_reply(input_text):
    data = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": input_text
            },
        },
        "userInfo": {
            "apiKey": "cc8c863cfa2b42ecb1e6ae9d4f2c5f36",
            "userId": "339745"
        }
    }

    data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    url = urllib.request.Request("http://openapi.tuling123.com/openapi/api/v2", data=data, method="POST")
    res = urllib.request.urlopen(url).read()

    return json.loads(res.decode("utf-8"))["results"][0]["values"]["text"]


app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/chat_robot', methods=['POST'])
def chat_robot():
    msg = flask.request.form.get('msg')
    # print(flask.request.form)
    # print(flask.request.headers)
    # print(flask.request.get_data())

    if msg is None:
        reply = 'error'
    else:
        try:
            reply = get_robot_reply(msg)
        except Exception as e:
            reply = str(e)

    return reply

if __name__ == '__main__':
    app.run(debug=True)
