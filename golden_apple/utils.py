import asyncio
import json
import os

from environs import Env
from aiohttp import ClientSession
import pandas as pd

from .db_client import get_products
from .models import ProductList, ProductData

env = Env()
env.read_env()

PAGES_URL = env('PAGES_URL')


async def get_json(session: ClientSession, url: str) -> json:
    async with session.get(url) as response:
        assert response.status == 200
        data = await response.json()
        return data


async def get_products_list(session: ClientSession, url: str) -> ProductList:
    data = await get_json(session, url)
    data = data['data']['products']
    return ProductList(**data)


async def get_products_ids(session: ClientSession) -> list:
    ids = []

    start_data = await get_products_list(session, f'{PAGES_URL}0')
    count = start_data.count
    ids.extend(start_data.products)

    if count % 24 == 0:
        last_page = count // 24 + 1
    else:
        last_page = (count // 24) + 2

    tasks = []
    for i in range(1, last_page):
        task = asyncio.create_task(get_products_list(session, f'{PAGES_URL}{i}'))
        tasks.append(task)

        if len(tasks) == 7:
            data = await asyncio.gather(*tasks)
            data = [i.products for i in data]
            data = sum(data, [])
            ids.extend(data)
            tasks = []
    else:
        if tasks:
            data = await asyncio.gather(*tasks)
            data = [i.products for i in data]
            data = sum(data, [])
            ids.extend(data)

    return ids


async def get_products_detail(session: ClientSession, url: str) -> tuple:
    data = await get_json(session, url)
    data = data['data']
    return ProductData(**data).to_tuple()


async def write_to_excel():
    golden_apple_path = os.path.dirname(__file__)
    data_path = os.path.join(golden_apple_path, '../data')
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    data = await get_products()
    columns = ['id', 'Название товара', 'Бренд', 'Тип товара', 'Цена', 'Описание', 'Применение', 'Состав', 'О бренде', 'Дополнительная информация']
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(f'{data_path}/data.xlsx', index=False, engine='xlsxwriter')
