import asyncpg
from environs import Env
from asyncpg import Connection


env = Env()
env.read_env()

DB_URL = env('DB_URL')


async def connection() -> Connection:
    conn = await asyncpg.connect(DB_URL)
    return conn


async def create_table():
    conn = await connection()
    await conn.execute("""CREATE TABLE IF NOT EXISTS golden_apple(
    id BIGSERIAL PRIMARY KEY,
    product_id varchar(200) unique,
    name varchar(500),
    brand varchar(500),
    product_type varchar(500),
    price INTEGER,
    description text,
    application text,
    composition text,
    about_brand text,
    addit_info text
    )""")

    await conn.close()


async def data_cleaner():
    conn = await connection()
    await conn.execute("""TRUNCATE TABLE golden_apple """)


async def insert_data(data: list) -> int:
    conn = await connection()
    await conn.executemany("""INSERT INTO golden_apple(product_id, name, brand, 
    product_type, price, description, application, composition, about_brand, 
    addit_info)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    ON CONFLICT (product_id) DO UPDATE SET price = excluded.price
    """, data)


    count = await conn.fetchval("""SELECT COUNT(*) FROM golden_apple """)
    await conn.close()

    return count

async def get_products():
    conn = await connection()
    result = await conn.fetch("""SELECT product_id, name, brand, 
    product_type, price, description, application, composition, about_brand, 
    addit_info FROM golden_apple""")
    await conn.close()

    return [list(i) for i in result]
