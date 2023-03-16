import aiohttp
import asyncio


async def test_api():
    url = 'http://localhost:8000/myviewset/api/'
    files = {'file': open('data.xlsx', 'rb')}
    data = {
        'article': '123456',

    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers={'Content-Type': 'application/json'}, timeout=60, ssl=False) as response:
            response_data = await response.json()
            print(response_data)

asyncio.run(test_api())
