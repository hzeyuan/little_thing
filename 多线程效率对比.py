import time
from threading import Thread

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


def io():
    write()
    read()


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
counts = []
t = time.time()
for x in range(0):
    thread = Thread(target=count, args=(1, 1))
    counts.append(thread)
    thread.start()
while 1:
    e = len(counts)
    for th in counts:
        if not th.is_alive():
            e -= 1
    if e <= 0:
        break
print("多线程 cpu", time.time() - t)

# IO密集操作
t = time.time()
ios = []
for x in range(0):
    thread = Thread(target=io)
    ios.append(thread)
    thread.start()
while True:
    e = len(ios)
    for th in ios:
        if not th.is_alive():
            e -= 1
    if e <= 0:
        break
print("多线程 IO", time.time() - t)


# 网络请求密集型操作
t = time.time()
request_list = []
for x in range(10):
    thread = Thread(target=http_request)
    request_list.append(thread)
    thread.start()

while True:
    e = len(request_list)
    for th in request_list:
        if not th.is_alive():
            e -= 1
    if e <= 0:
        break
print("Thread Http Request", time.time() - t)
