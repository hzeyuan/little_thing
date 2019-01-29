"""
时间：
Cost:1.4321117401123047 seconds
Cost:0.7483363151550293 seconds
Cost 0.6141154766082764 seconds


"""

from lxml import etree
from time import time
import asyncio
import aiohttp

url = 'https://movie.douban.com/top250'


# 抓取页面内容
async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


# 解析页面内容
async def parse(url):
    page = await fetch_content(url)
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

    tasks = [fetch_content(url) for url in fetch_list]
    pages = await asyncio.gather(*tasks)

    for page in pages:
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text
        print(i, title)


def main():
    loop = asyncio.get_event_loop()
    start = time()
    loop.run_until_complete(parse(url))
    end = time()
    print('Cost {} seconds'.format(end - start))
    loop.close()


if __name__ == '__main__':
    main()
