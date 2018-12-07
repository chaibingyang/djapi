# 接口帮助文档

### 智能聊天

**接口地址：**http://api.itmojun.com/chat_robot

**返回格式：**text

**请求方式：**post

**请求示例：**http://api.itmojun.com/chat_robot

   

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

**接口地址：**http://api.itmojun.com/idcard

**返回格式：**json

**请求方式：**get

**请求示例：**http://api.itmojun.com/idcard?cardno=330326198903081211

   

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
  "birthday": "1989年03月08日"
  "sex": "男"
}
```