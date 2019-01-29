import time
from multiprocessing import Process

import requests


# CPU密集运算
def count(x, y):
    c = 0
    while c < 500000:
        c += 1
        x += x
        y += y
    print(y)


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


if __name__ == '__main__':
    counts = []
    t = time.time()
    for x in range(0):
        process = Process(target=count, args=(1, 1))
        counts.append(process)
        process.start()

    while True:
        e = counts.__len__()
        for th in counts:
            if not th.is_alive():
                e -= 1
        if e <= 0:
            break

    print("Multiprocess cpu", time.time() - t)

    t = time.time()
    ios = []
    for x in range(0):
        process = Process(target=io)
        ios.append(process)
        process.start()

    while True:
        e = ios.__len__()
        for th in ios:
            if not th.is_alive():
                e -= 1
        if e <= 0:
            break
    print("Multiprocess IO", time.time() - t)
    t = time.time()  #
    httprs = []
    for x in range(10):
        process = Process(target=http_request)
        httprs.append(process)
        process.start()

    while True:
        e = httprs.__len__()
        for th in httprs:
            if not th.is_alive():
                e -= 1
        if e <= 0:
            break
    print("Multiprocess Http Request", time.time() - t)
