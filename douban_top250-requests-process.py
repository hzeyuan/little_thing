"""
时间：
Cost:25.425570011138916 Seconds
Cost:28.839136123657227 Seconds
"""

import requests
from lxml import etree
from concurrent.futures import ProcessPoolExecutor

url = 'https://movie.douban.com/top250'


def fetch_page(url):
    response = requests.get(url)
    return response


def fetch_content(url):
    response = fetch_page(url)
    page = response.content
    return page


def parse(url):
    page = fetch_content(url)
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

    with ProcessPoolExecutor(max_workers=10) as executor:
        for page in executor.map(fetch_content, fetch_list):
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
