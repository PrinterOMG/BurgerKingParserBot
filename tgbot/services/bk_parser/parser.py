import asyncio
import logging
from pprint import pprint

import aiohttp


class AuthError(Exception):
    pass


class ApiError(Exception):
    pass


class BurgerKingParser:
    def __init__(self, token=''):
        self.token = token

        self.headers = {
            'X-Burger-King-Token': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    def update_token(self, new_token):
        self.token = new_token
        self.headers['X-Burger-King-Token'] = new_token

    async def get_user_info(self):
        url = 'https://burgerkingrus.ru/auth/v1/user/info'

        return await self._get_request(url)

    async def get_user_check_info(self):
        url = 'https://burgerkingrus.ru/secret-shopper/api/v1/user/info'

        return await self._get_request(url)

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

            try:
                async with request(url, **kwargs) as response:
                    json_resp = await response.json()
            except:
                logging.error(await response.text())
                raise ApiError
            else:
                if 'message' in json_resp and json_resp['message'] == 'Ошибка авторизации':
                    logging.error(json_resp)
                    raise AuthError

                return json_resp


async def main():
    bk = BurgerKingParser('27846d7e-0d29-4bd0-bb06-1283210673f7')

    pprint(await bk.parse_restaurant_dates(436))


if __name__ == '__main__':
    asyncio.run(main())
