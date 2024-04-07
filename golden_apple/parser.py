import asyncio
from random import shuffle

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from funcy import chunks
from tqdm import tqdm
from environs import Env

from .config import HEADERS
from .utils import get_products_ids, get_products_detail, write_to_excel
from .db_client import insert_data, data_cleaner, create_table


env = Env()
env.read_env()


PROD_URL = env('PROD_URL')


async def main():

    logger.info('Парсинг начался...')
    await create_table()
    await data_cleaner()
    async with ClientSession(headers=HEADERS, timeout=ClientTimeout(total=60)) as session:     #открываем клиентскую сессию, для похода на сайт
        logger.info('Получаем ID товара...')
        ids = await get_products_ids(session)
        logger.info(f'Найдено {len(ids)} товаров')

        shuffle(ids) # Перемешиваем айдишники
        for chunk in tqdm(list(chunks(7, ids))):
            tasks = []
            for i in chunk:
                task = asyncio.create_task(get_products_detail(session, PROD_URL % i))
                tasks.append(task)
            data = await asyncio.gather(*tasks)
            count_saved_data = await insert_data(data)
            logger.info(f'Сохранено {count_saved_data} товаров')

    await write_to_excel()
    logger.info('Парсинг успешно завершен!')








