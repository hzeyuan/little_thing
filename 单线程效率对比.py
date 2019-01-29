import time

import requests


# CPU密集运算
def count(x, y):
    c = 0
    while c < 500000:
        c += 1
        x += x
        y += y


# io文件读取
def write():
    f = open('test.txt', 'w')
    for x in range(500000):
        f.write('testwrite\n')
    f.close()


def read():
    f = open('test.txt', 'r')
    lines = f.readlines()
    f.close()


# requests网络请求
url = 'http://www.tieba.com'


def http_request():
    try:
        r = requests.get(url)
        text = r.text
        return {'context': text}
    except Exception as e:
        return {'error': e}


# CPU密集操作

t = time.time()
for x in range(0):
    count(1, 1)
print("Line cpu", time.time() - t)

# IO密集操作
t = time.time()
for x in range(10):
    write()
    read()
print("Line IO", time.time() - t)

# 网络请求密集型操作
t = time.time()
for x in range(5):
    http_request()
print("Line Http Request", time.time() - t)
