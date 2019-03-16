# 接口帮助文档

（注意：所有接口都同时支持http和https两种访问方式，并且都支持跨域调用）

### 智能聊天

**接口地址：** [http://api.itmojun.com/chat_robot](http://api.itmojun.com/chat_robot)

**返回格式：** text

**请求方式：** post

**请求示例：** [http://api.itmojun.com/chat_robot](http://api.itmojun.com/chat_robot)

**跨域调用：** 支持

   

请求参数说明：

（注意：POST数据要采用x-www-form-urlencoded编码，和普通网页表单数据提交的编码方式一样，例如：如果msg的内容为“你好”，那么编码之后为：msg=%E4%BD%A0%E5%A5%BD）

| 名称 | 必填 | 类型   | 说明     |
| ---- | ---- | ------ | -------- |
| msg  | Y    | string | 聊天内容 |



返回参数说明：智能聊天回复内容，MIME类型为：text/plain; charset=utf-8



Python调用示例：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

while True:
    msg = input('\n我说：')
    reply = requests.post('http://api.itmojun.com/chat_robot', {'msg': msg}).text
    print('\n小智说：' + reply)
```





### 根据身份证号码获取对应的地址区域、生日和性别信息

**接口地址：** [http://api.itmojun.com/idcard](http://api.itmojun.com/idcard)

**返回格式：** json

**请求方式：** get

**请求示例：** [http://api.itmojun.com/idcard?cardno=330326198903081211](http://api.itmojun.com/idcard?cardno=330326198903081211)

**跨域调用：** 支持

   

请求参数说明：

| 名称   | 必填 | 类型   | 说明       |
| ------ | ---- | ------ | ---------- |
| cardno | Y    | string | 身份证号码 |



返回参数说明：

| 名称     | 类型   | 说明                         |
| -------- | ------ | ---------------------------- |
| err      | int    | 错误码，0表示成功，1表示失败 |
| area     | string | 地区                         |
| birthday | string | 出生日期                     |
| sex      | string | 性别                         |



JSON返回示例：

```
{
  "err": 0,
  "area": "浙江省温州市平阳县",
  "birthday": "1989年03月08日",
  "sex": "男"
}
```




### 向执行设备发送控制命令

**接口地址：** [http://api.itmojun.com/device/cmd/send](http://api.itmojun.com/device/cmd/send)

**返回格式：** text/plain; charset=utf-8

**请求方式：** get

**请求示例：** [http://api.itmojun.com/device/cmd/send?user_id=dj&dev_id=pc&content=poweroff](http://api.itmojun.com/device/cmd/send?user_id=dj&dev_id=pc&content=poweroff)

**跨域调用：** 支持

   

请求参数说明：

| 名称    | 必填 | 类型   | 说明                       |
| ------- | ---- | ------ | -------------------------- |
| user_id | Y    | string | 用户ID，比如dj             |
| dev_id  | Y    | string | 设备ID，比如pc、relay等    |
| content | Y    | string | 控制命令内容，比如poweroff |



返回参数说明：执行成功返回ok，失败返回err





### 执行设备获取控制命令

**接口地址：** [http://api.itmojun.com/device/cmd/get](http://api.itmojun.com/device/cmd/get)

**返回格式：** text/plain; charset=gbk（字符集为gbk是为了方便Visual C++进行处理）

**请求方式：** get

**请求示例：** [http://api.itmojun.com/device/cmd/get?user_id=dj&dev_id=pc](http://api.itmojun.com/device/cmd/get?user_id=dj&dev_id=pc)

**跨域调用：** 支持

   

请求参数说明：

| 名称    | 必填 | 类型   | 说明                    |
| ------- | ---- | ------ | ----------------------- |
| user_id | Y    | string | 用户ID，比如dj          |
| dev_id  | Y    | string | 设备ID，比如pc、relay等 |



返回参数说明：获取到的最新控制命令内容，如果没有控制命令内容则返回空字符串

备注：通过上面的发送控制命令接口发送的控制命令会在10秒后失效，所以发送控制命令后要及时调用本接口，另外成功调用本接口一次后相应的控制命令内容就被删除了，即一个控制命令内容最多只能被获取一次





### 传感器设备上传采集到的数据

**接口地址：** [http://api.itmojun.com/device/data/upload](http://api.itmojun.com/device/data/upload)

**返回格式：** text/plain; charset=utf-8

**请求方式：** get

**请求示例：** [http://api.itmojun.com/device/data/upload?user_id=dj&dev_id=dht11&content=15_60](http://api.itmojun.com/device/data/upload?user_id=dj&dev_id=dht11&content=15_60)

**跨域调用：** 支持

   

请求参数说明：

| 名称    | 必填 | 类型   | 说明                             |
| ------- | ---- | ------ | -------------------------------- |
| user_id | Y    | string | 用户ID，比如dj                    |
| dev_id  | Y    | string | 设备ID，比如dht11、light等      |
| content | Y    | string | 传感器采集到的数据，有以下情况：<br>1. 对于温湿度传感器（比如DHT11等），格式为：温度值_湿度值<br>2. 对于光照传感器，其内容就是光照强度值 |



返回参数说明：执行成功返回ok，失败返回err





### 查询传感器设备上传的最新数据

**接口地址：** [http://api.itmojun.com/device/data/query](http://api.itmojun.com/device/data/query)

**返回格式：** json

**请求方式：** get

**请求示例：** [http://api.itmojun.com/device/data/query?user_id=dj&dev_id=dht11](http://api.itmojun.com/device/data/query?user_id=dj&dev_id=dht11)

**跨域调用：** 支持



请求参数说明：

| 名称    | 必填 | 类型   | 说明                       |
| ------- | ---- | ------ | -------------------------- |
| user_id | Y    | string | 用户ID，比如dj             |
| dev_id  | Y    | string | 设备ID，比如dht11、light等 |



返回参数说明：

| 名称    | 类型   | 说明                                                         |
| ------- | ------ | ------------------------------------------------------------ |
| err     | int    | 错误码，0表示成功，1表示失败（此时content和time字段为空字符串） |
| content | string | 传感器设备上传的数据，有以下情况：<br>1. 对于温湿度传感器（比如DHT11等），格式为：温度值_湿度值<br>2. 对于光照传感器，其内容就是光照强度值 |
| time    | string | 传感器设备上传数据的时间（上传数据到达服务器的时间），格式为：YYYY-MM-DD HH:MM:SS，比如2018-12-22 18:18:05 |



JSON返回示例：

```
{
  "err": 0,
  "content": "15_60",
  "time": "2018-12-22 18:18:05"
}
```




### 向PC机上运行的程序发送控制命令

**接口地址：** [http://api.itmojun.com/pc/cmd/send](http://api.itmojun.com/pc/cmd/send)

**返回格式：** text/plain; charset=utf-8

**请求方式：** get

**请求示例：** [http://api.itmojun.com/pc/cmd/send?id=dj&content=poweroff](http://api.itmojun.com/pc/cmd/send?id=dj&content=poweroff)

**跨域调用：** 支持

   

请求参数说明：

| 名称    | 必填 | 类型   | 说明                                                   |
| ------- | ---- | ------ | ------------------------------------------------------ |
| id      | Y    | string | PC机上运行的程序的ID，用来唯一地标识不同的程序，比如dj |
| content | Y    | string | 控制命令内容，比如poweroff |



返回参数说明：执行成功返回ok，失败返回err




### PC程序从平台获取最新的控制命令

**接口地址：** [http://api.itmojun.com/pc/cmd/get](http://api.itmojun.com/pc/cmd/get)

**返回格式：** text/plain; charset=gbk（字符集为gbk是为了方便Visual C++进行处理）

**请求方式：** get

**请求示例：** [http://api.itmojun.com/pc/cmd/get?id=dj](http://api.itmojun.com/pc/cmd/get?id=dj)

**跨域调用：** 支持

   

请求参数说明：

| 名称    | 必填 | 类型   | 说明                                                   |
| ------- | ---- | ------ | ------------------------------------------------------ |
| id      | Y    | string | PC机上运行的程序的ID，用来唯一地标识不同的程序，比如dj |



返回参数说明：获取到的最新控制命令内容，如果没有控制命令内容则返回空字符串

备注：通过上面的发送控制命令接口发送的控制命令会在3秒后失效，所以发送控制命令后要及时调用本接口，另外建议每隔3秒调用一次本接口，否则可能多次接收到重复的控制命令内容



### 基于MQTT协议发布消息

**接口地址：** [http://api.itmojun.com/mqtt](http://api.itmojun.com/mqtt)

**返回格式：** text/plain; charset=utf-8

**请求方式：** post

**跨域调用：** 支持



请求参数说明：

| 名称    | 必填 | 类型   | 说明                                          |
| ------- | ---- | ------ | --------------------------------------------- |
| topic   | Y    | string | 消息的主题，比如：/smart_house/dj/temperature |
| payload | Y    | string | 消息的内容，比如：28℃                         |



返回参数说明：执行成功返回ok，失败返回err



### 在线二维码生成器

**接口地址：** [http://api.itmojun.com/qr](http://api.itmojun.com/qr)

**返回格式：** image/png

**请求方式：** get

**请求示例：** [http://api.itmojun.com/qr?text=IT魔君](http://api.itmojun.com/qr?text=IT魔君)

**跨域调用：** 支持



请求参数说明：

| 名称    | 必填 | 类型   | 说明                                          |
| ------- | ---- | ------ | --------------------------------------------- |
| text   | Y    | string | 要编码成二维码图像的数据内容 |   



调用示例：

```
<img src="https://api.itmojun.com/qr?text=IT魔君" />
```
