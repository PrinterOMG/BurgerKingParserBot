import asyncio
from pprint import pprint

import aiohttp


class BurgerKingParser:
    restaurants = {
        466: 'Казань, просп Ямашева 97, ТЦ XL 4 этаж',
        279: 'Казань, просп Ибрагимова 56, ТЦ Тандем 3 этаж',
        436: 'Казань, ул Декабристов 133, ТЦ Тюбетейка',
        321: 'Казань, просп Хусаина Ямашева 46, ТЦ Парк Хаус 2 этаж'
    }

    def __init__(self, token):
        self.token = token

        self.headers = {
            'X-Burger-King-Token': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    async def parse_restaurants_dates(self):
        results = dict()
        for rest_id, rest_name in self.restaurants.items():
            dates = await self.parse_restaurant_dates(rest_id)
            results[rest_id] = {
                'name': rest_name,
                'dates': dates['dates']
            }
        return results

    async def parse_restaurant_dates(self, restaurant_id):
        url = f'https://burgerkingrus.ru/secret-shopper/api/v1/check/available/dates?restaurant={restaurant_id}&checkType=restaurant'

        return await self._get_request(url)

    async def _get_request(self, url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                return await response.json()


async def main():
    bk = BurgerKingParser('123')
    pprint(await bk.parse_restaurants_dates())


if __name__ == '__main__':
    asyncio.run(main())
