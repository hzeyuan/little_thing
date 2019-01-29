"""
完整的请求-相应模型
import urllib
#请求
request = urllib.request.Request('https://www.baidu,com')
#响应
response = urllib.request.urlopen(request)
html = response.read()
print（html）
------------
添加请求头:

headers = {'User_Agent':'xxxx','xxx':'xxxx'}
使用add_header或者在urllib.request.Request(url，headers)
---------
时间：
Cost 61.70986485481262 seconds
Cost 43.65137505531311 seconds
"""
import urllib.request
import ssl
from lxml import etree

url = 'https://movie.douban.com/top250'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)

url_agent = 'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1'


def fetch_page(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', url_agent)
    response = urllib.request.urlopen(req, context=context)
    return response


def parse(url):
    response = fetch_page(url)
    page = response.read()
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

    for url in fetch_list:
        response = fetch_page(url)
        page = response.read()
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text
        print(i, title)


def main():
    from time import time
    start = time()
    parse(url)
    end = time()
    print(f'Cost {end - start} seconds')


if __name__ == '__main__':
    main()
