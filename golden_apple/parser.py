import asyncio
import json

from aiohttp import ClientSession
from loguru import logger
from pprint import pprint

from .config import HEADERS, PAGES_URL
from .utils import get_json
from .models import ProductList




async def main():
    ids = []
    async with ClientSession(headers=HEADERS) as session:     #открываем клиентскую сессию, для похода на сайт
        start_data = await get_json(session, f'{PAGES_URL}1')
        start_data = start_data['data']['products']
        start_data = ProductList(**start_data)
        count = start_data.count
        ids.extend(start_data.products)

        if count % 24 == 0:
            last_page = count // 24 + 1
        else:
            last_page = (count // 24) + 2

        tasks = []
        for i in range(2, last_page):
            task = asyncio.create_task(get_json(session, f'{PAGES_URL}{i}'))
            tasks.append(task)

        data = await asyncio.gather(*tasks)
        data = [ProductList(**i['data']['products']) for i in data]
        data = [i.products for i in data]
        data = sum(data, [])
        ids.extend(data)
        pprint(ids)





        # async with session.get('https://goldapple.ru/front/api/catalog/plp?categoryId=1000003870&cityId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5&geoPolygons[]=EKB-000000347&geoPolygons[]=EKB-000000367&geoPolygons[]=EKB-000000360&geoPolygons[]=EKB-000000356&pageNumber=1') as response:
        #     logger.info(response.status)
        #     data = await response.json()
        #     data = data['data']['products']
        #     with open('test.json', 'w', encoding='utf-8') as file:
        #         json.dump(data, file, ensure_ascii=False, indent=2)
        #     # pprint(data)
