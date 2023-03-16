import asyncio
from typing import List

from aiohttp import ClientSession
from pydantic import BaseModel


class ResponseSerializer(BaseModel):
    article: str
    brand: str
    title: str

    class Config:
        orm_mode = True


class ResponseListSerializer(BaseModel):
    data: List[ResponseSerializer]

    class Config:
        orm_mode = True


def url_gen(bucket, article):
    return f'https://basket-0{bucket}.wb.ru/vol{article[:3]}/part{article[:5]}/{article}/info/ru/card.json'


async def get_product_data(session: ClientSession, article: str):
    for i in range(1, 10):
        try:
            url = url_gen(i, article)
            async with session.get(url) as response:
                data = await response.json()
                print(data)
                brand = data['selling']['brand_name']
                title = data['imt_name']
                return ResponseSerializer(article=article, brand=brand, title=title)
        except Exception:
            pass


async def collect_data(articles: List[str]) -> ResponseListSerializer:
    async with ClientSession() as session:
        tasks = [get_product_data(session, article) for article in articles]
        results = await asyncio.gather(*tasks)
        data = []
        for result in results:
            print(result)
            if result:
                data.append(result)
        return ResponseListSerializer(data=data)


def get_product_data_list(articles):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if type(articles) == str:
        result = loop.run_until_complete(get_product_data(ClientSession(), articles))
    else:
        result = loop.run_until_complete(collect_data(articles))
    return result
