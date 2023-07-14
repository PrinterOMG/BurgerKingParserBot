import asyncio
from pprint import pprint

import aiohttp


class AuthError(Exception):
    pass


class BurgerKingParser:
    restaurants = {
        466: 'Казань, просп Ямашева 97, ТЦ XL 4 этаж',
        279: 'Казань, просп Ибрагимова 56, ТЦ Тандем 3 этаж',
        436: 'Казань, ул Декабристов 133, ТЦ Тюбетейка',
        321: 'Казань, просп Хусаина Ямашева 46, ТЦ Парк Хаус 2 этаж'
    }

    def __init__(self, token=''):
        self.token = token

        self.headers = {
            'X-Burger-King-Token': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    def update_token(self, new_token):
        self.token = new_token
        self.headers['X-Burger-King-Token'] = new_token

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

    async def get_cities(self, limit=-1):
        url = f'https://burgerkingrus.ru/secret-shopper/api/v1/city/list?limit={limit}'

        return await self._get_request(url)


    async def get_city_restaurants(self, city_id):
        url = f'https://burgerkingrus.ru/secret-shopper/api/v1/restaurant?city={city_id}'

        return await self._get_request(url)

    async def start_login(self, phone: str, retry=False):
        url = 'https://burgerkingrus.ru/auth/v3/auth/login'
        payload = {
            'phone': phone,
            'retry': retry
        }

        return await self._post_request(url, payload, requires_token=False)

    async def get_token(self, phone, code, login_hash, firebase='', platform=0):
        url = 'https://burgerkingrus.ru/auth/v3/auth/token'
        payload = {
            'phone': phone,
            'code': code,
            'hash': login_hash,
            'firebase': firebase,
            'platform': platform
        }

        return await self._post_request(url, payload, requires_token=False)

    async def _get_request(self, url, requires_token=True):
        return await self._request('GET', url, requires_token)

    async def _post_request(self, url, payload, requires_token=True):
        return await self._request('POST', url, requires_token, json=payload)

    async def _request(self, method, url, requires_token, **kwargs):
        if method not in ('POST', 'GET', 'PUT', 'DELETE', 'PATCH'):
            raise ValueError(f'Unknown method "{method}"')

        if requires_token and not self.token:
            raise AuthError

        async with aiohttp.ClientSession(headers=self.headers) as session:
            match method:
                case 'POST': request = session.post
                case 'GET': request = session.get
                case 'PUT': request = session.put
                case 'DELETE': request = session.delete
                case 'PATCH': request = session.patch

            async with request(url, **kwargs) as response:
                json_resp = await response.json()

                if 'message' in json_resp and json_resp.message == 'Ошибка авторизации':
                    raise AuthError

                return json_resp


async def main():
    bk = BurgerKingParser()

    phone = input('Input phone: ')
    login = await bk.start_login(phone)
    pprint(login)
    if login['status'] != 'ok':
        return

    code = input('Input code: ')
    token = await bk.get_token(phone, code, login['response']['hash'])
    pprint(token)
    token = token['response']['token']
    bk.update_token(token)

    result = await bk.get_city_restaurants(1)
    pprint(result)
    print(len(result))


if __name__ == '__main__':
    asyncio.run(main())
