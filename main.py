#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: dj
@contact: dj@itmojun.com
@software: PyCharm
@file: main.py
@time: 2018/12/5 20:32
"""

import time, re, json
import urllib
from io import BytesIO
import flask
from werkzeug.contrib.fixers import ProxyFix
import redis
import paho.mqtt.publish as publish
import qrcode


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


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


# 函数功能：获取指定身份证号的相关信息（包括行政区域，生日，性别）
# 参数：
#   cardno str, 合法的身份证号
# 返回值：
#   字典类型，格式为：{"err": 0, "area": "湖北省武汉市江夏区", "birthday": "1990年8月13日", "sex": "男"}
#   如果err字段为0，表示获取信息成功，为1表示获取信息失败（原因可能是身份证号位数错误、含有非法字符、校验码错误、行政区域不存在）
def get_idcard_info(cardno):
    ret = {"err": 1, "area": "", "birthday": "", "sex": ""}

    # 初级校验
    cardno = cardno.upper()
    if re.fullmatch("[1-6]\\d{16}[\\d|X]", cardno) == None:
        return ret

    # 利用身份证号最末尾的校验码进一步校验
    code = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    i, s = 0, 0
    while i < 17:
        s += int(cardno[i]) * code[i]
        i += 1

    s = (12 - (s % 11)) % 11

    if s == 10:
        s = "X"
    else:
        s = str(s)

    if s != cardno[17]:
        return ret

    # 提取身份证号中的信息
    area_code = cardno[:6]
    with open("./idcard_addr_code.txt", "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line == "":
                break

            if line[:6] == area_code:
                ret["area"] = line.split()[1]
                break

    birthday = cardno[6:14]
    birthday = "%s年%d月%d日" % (birthday[0:4], int(birthday[4:6]), int(birthday[6:8]))
    ret["birthday"] = birthday

    sex = "男"
    if int(cardno[-2]) % 2 == 0:
        sex = "女"
    ret["sex"] = sex

    if ret["area"] != "" and ret["birthday"] != "" and ret["sex"] != "":
        ret["err"] = 0

    return ret


app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['JSON_AS_ASCII'] = False  # 如果不加这行配置，那么jsonify函数生成的json字符串中所有非ASCII字符都会表示为\u这种形式，json.dumps()解决同样的问题可以加入ensure_ascii=False
app.config['JSON_SORT_KEYS'] = False  # jsonify函数不对key进行自动排序，默认会自动排序

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

    return reply, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route("/idcard")
def idcard():
    cardno = flask.request.args.get("cardno", "")
    card_info = get_idcard_info(cardno)
    # return json.dumps(card_info, ensure_ascii=False)  # 这种写法Content-Type为默认的text/html; charset=utf-8
    # return flask.Response(json.dumps(card_info, ensure_ascii=False), mimetype='application/json; charset=utf-8')  # 返回Response对象
    # return json.dumps(card_info, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}  # 返回元组，和上面的写法等效
    return flask.jsonify(card_info)  # 这种写法Content-Type为application/json(后面没有charset=utf-8，默认编码为utf-8)


@app.route("/device/cmd/<operation>")
def dev_cmd(operation):
    user_id = flask.request.args.get("user_id", "")
    dev_id = flask.request.args.get("dev_id", "")
    redis_key = "cmd " + user_id + " " + dev_id

    if operation == "send":
        content = flask.request.args.get("content", "")
        r = redis.Redis(connection_pool=pool)
        ret = r.set(redis_key, content, ex=10)  # 过期时间为10秒
        if(ret):
            ret = "ok"
        else:
            ret = "err"
        return ret, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    elif operation == "get":
        r = redis.Redis(connection_pool=pool)
        ret = r.get(redis_key)
        if ret is None:
            return "", 200, {'Content-Type': 'text/plain; charset=gbk'}
        else:
            r.delete(redis_key)
            return ret.encode("gbk"), 200, {'Content-Type': 'text/plain; charset=gbk'}


@app.route("/device/data/<operation>")
def dev_data(operation):
    user_id = flask.request.args.get("user_id", "")
    dev_id = flask.request.args.get("dev_id", "")
    redis_key = "data " + user_id + " " + dev_id

    if operation == "upload":
        content = flask.request.args.get("content", "")
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        r = redis.Redis(connection_pool=pool)
        ret = r.hmset(redis_key, {"content": content, "time": cur_time})

        if ret:
            ret = "ok"
        else:
            ret = "err"
            
        return ret, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    elif operation == "query":
        r = redis.Redis(connection_pool=pool)
        data = {"err": 1, "content": "", "time": ""}

        if r.exists(redis_key):
            data["err"] = 0
            data["content"] = r.hget(redis_key, "content")
            data["time"] = r.hget(redis_key, "time")

        return flask.jsonify(data)  # 这种写法Content-Type为application/json(后面没有charset=utf-8，默认编码为utf-8)


@app.route("/pc/cmd/<operation>")
def pc_cmd(operation):
    pc_id = flask.request.args.get("id", "")
    redis_key = pc_id

    if operation == "send":
        content = flask.request.args.get("content", "")
        r = redis.Redis(connection_pool=pool)
        ret = r.set(redis_key, content, ex=3)  # 过期时间为3秒
        if(ret):
            ret = "ok"
        else:
            ret = "err"
        return ret, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    elif operation == "get":
        r = redis.Redis(connection_pool=pool)
        ret = r.get(redis_key)
        if ret is None:
            return "", 200, {'Content-Type': 'text/plain; charset=gbk'}
        else:
            # r.delete(redis_key)
            return ret.encode("gbk"), 200, {'Content-Type': 'text/plain; charset=gbk'}


@app.route('/mqtt', methods=['POST'])
def mqtt_server():
    # flask.request.args.get方法只能获取url中的参数，不能获取请求体中的数据，所以不能用于这里
    topic = flask.request.form.get('topic')
    payload = flask.request.form.get('payload')

    if topic is None:
        reply = 'err'
    else:
        publish.single(topic, payload, hostname="localhost", port=1883)
        reply = 'ok'

    return reply, 200, {'Content-Type': 'text/plain; charset=utf-8'}


# 在线二维码生成接口
@app.route("/qr")
def gen_qrcode():
    # 获得HTTP请求中的URL参数（参数名称为text）
    text = flask.request.args.get("text")

    # 创建BytesIO对象，用于存放二维码图像数据
    bi = BytesIO()
    img = qrcode.make(text)  # 生成二维码图像
    img.save(bi, "png")  # 将二维码图像以png编码格式写入bi对象
    bi.seek(0)  # 移动bi对象的位置指针到开头

    # 将二维码图像数据发送给浏览器
    return flask.send_file(bi, "image/png")


@app.after_request
def af_request(resp):
    # 请求钩子，在每个请求发生后自动执行，这里用于设置header，实现跨域

    resp = flask.make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
