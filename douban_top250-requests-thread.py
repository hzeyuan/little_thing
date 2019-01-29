"""
---------
时间：
Cost:12.211171627044678 seconds
Cost:21.3074848651886 seconds
"""


import requests
from lxml import etree
from threading import Thread


def fetch_page(url):
    r = requests.get(url)
    return r.content


def parse(url):
    page = fetch_page(url)
    html = etree.HTML(page)

    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'

    pages = html.xpath(xpath_pages)
    fetch_list = []
    result = []

    for element_movie in html.xpath(xpath_movie):
        result.append(element_movie)

    for p in pages:
        fetch_list.append(url + p.get('href'))

    def fetch_content(url):
        page = fetch_page(url)
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    threads = []
    for url in fetch_list:
        t = Thread(target=fetch_content, args=[url])
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

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
