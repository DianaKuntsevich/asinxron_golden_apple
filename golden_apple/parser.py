import asyncio
import json

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from pprint import pprint
from funcy import chunks
from tqdm import tqdm

from .config import HEADERS, PAGES_URL, PROD_URL
from .utils import get_products_ids, get_json, get_products_detail
from .models import ProductList


async def main():
    async with ClientSession(headers=HEADERS, timeout=ClientTimeout(total=60)) as session:     #открываем клиентскую сессию, для похода на сайт
        ids = await get_products_ids(session)

        for chunk in tqdm(list(chunks(7, ids))):
            tasks = []
            for i in chunk:
                task = asyncio.create_task(get_products_detail(session, PROD_URL % i))
                tasks.append(task)
            data = await asyncio.gather(*tasks)
            print(data)









