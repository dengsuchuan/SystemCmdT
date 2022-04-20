# -*- coding: utf-8 -*-
from ast import arg, keyword
import uuid
import requests
import hashlib
import time
import json
import sys
from pyperclip import copy

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '75e01aa63fd8f226'
APP_SECRET = 'PF9A611RhCnHupjngrtUP4xl5Jc2sUUG'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(q):
    data = {}
    data['from'] = 'auto'
    data['to'] = 'auto'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = ""

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
        return response.content.decode('utf-8')
    else:
      return response.content.decode('utf-8')

if __name__ == '__main__':
    keyword = sys.argv[1]
    try:
        content = connect(keyword)
        json_data = json.loads(content)
    except Exception as e:
        print("翻译失败:", e)
        exit(1)

    print("全文翻译："+json_data['translation'][0])
    if 'web' in json_data:
        for item in json_data['web']:
            print(item['key'], item['value'])
            copyT = json_data['web'][0]['value'][0]
        try:
            copy(copyT)
            print("剪贴板获得："+copyT)
        except:
            print("剪贴板赋值失败："+copyT)
    else:
        print("没有网络释义")

    
    



  
