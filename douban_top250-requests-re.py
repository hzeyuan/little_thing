"""

-----------
时间：
275条
Cost:39.49648118019104 seconds
Cost:57.096041679382324 seconds
Cost:53.38093709945679 seconds
"""

import requests
import re

headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept - Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;'
                         'rv:2.0.1)Gecko/20100101Firefox/4.0.1'}


def fetch_page(url):
    r = requests.get(url, headers=headers)
    return r.content


def parse(url):
    page = fetch_page(url)
    fetch_list = []
    result = []

    for title in re.findall(rb'<a href=.*\s.*<span class="title">(.*)</span>', page):
        result.append(title)

    for postfix in re.findall(rb'<a href="(\?start=.*?)"', page):
        fetch_list.append(url + postfix.decode())

    for url in fetch_list:
        page = fetch_page(url)
        for title in re.findall(rb'<a href=.*\s.*<span class="title">(.*)</span>', page):
            result.append(title)

    for i, title in enumerate(result, 1):
        title = title.decode()
        print(i, title)


def main():
    from time import time
    url = 'https://movie.douban.com/top250'
    start = time()
    parse(url)
    end = time()
    print(f'Cost:{end-start}')


if __name__ == '__main__':
    main()
