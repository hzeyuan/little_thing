"""
一个完整的requests模型
r = requests.get(url)
content = r.content
page = etree.HTML(content)
page.xpath((节点))
---------
时间：
250条
Cost 43.597519397735596 seconds
Cost 38.67402100563049 seconds
Cost 34.001662492752075 seconds
"""

import requests
from lxml import etree

headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept - Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection': 'Keep-Alive',
           'User-Agent': 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'}


def fetch_page(url):
    r = requests.get(url, headers=headers)
    return r.content


def parse(url):
    page = fetch_page(url)
    fir_page = etree.HTML(page)
    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'
    pages = fir_page.xpath(xpath_pages)
    fetch_list = []
    result = []

    for element_movie in fir_page.xpath(xpath_movie):
        result.append(element_movie)

    for p in pages:
        fetch_list.append(url + p.get('href'))

    for url in fetch_list:
        page = fetch_page(url)
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text
        print(i, title)


def main():
    from time import time
    url = 'https://movie.douban.com/top250'
    start = time()
    parse(url)
    end = time()
    print(f'{end - start}')


if __name__ == '__main__':
    main()