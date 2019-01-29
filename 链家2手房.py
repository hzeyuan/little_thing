"""
----
2940条：
Cost 3.7898309230804443 seconds
"""
from lxml import etree
from time import time
import asyncio
import aiohttp

url = 'https://hui.lianjia.com/ershoufang/'


# 抓取页面内容
async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


# 解析页面内容
async def parse(url):

    xpath_house = "//div[@class='info clear']/div[@class='title']/a"
    xpath_house_price = "//div[@class='totalPrice']/span"
    # xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'

    fetch_list = []
    result = []

    for p in range(1, 11):
        fetch_list.append(url + f'//pg{p}//')

    tasks = [fetch_content(url) for url in fetch_list]
    pages = await asyncio.gather(*tasks)

    for page in pages:
        html = etree.HTML(page)
        for element_house, element_house_price in zip(html.xpath(xpath_house), html.xpath(xpath_house_price)):
            result.append(f'{element_house.text}:{element_house_price.text}万')

    for i, house in enumerate(result, 1):
        print(i, house)


def main():
    loop = asyncio.get_event_loop()
    start = time()
    loop.run_until_complete(parse(url))
    end = time()
    print('Cost {} seconds'.format(end - start))
    loop.close()


if __name__ == '__main__':
    main()
