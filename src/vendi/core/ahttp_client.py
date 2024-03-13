import aiohttp


class AsyncHTTPClient:
    def __init__(self, base_url: str, timeout: int = 60):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "content-type": "application/json",
        }

    def set_auth_header(self, access_key: str | None = None, jwt: str | None = None):
        if access_key:
            self.headers["x-api-key"] = access_key
        if jwt:
            self.headers["Authorization"] = f"Bearer {jwt}"

    async def get(self, path: str, params: dict = None) -> dict:
        url = self.base_url + path
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, params=params, timeout=self.timeout, headers=self.headers
            ) as response:
                return await self._handle_response(response)

    async def post(self, path: str, data: dict = None, headers: dict = None, **kwargs) -> dict:
        url = self.base_url + path
        _headers = self.headers
        if headers:
            _headers.update(headers)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, data=data, timeout=self.timeout, headers=_headers, **kwargs
            ) as response:
                return await self._handle_response(response)

    async def put(self, path: str, data: dict = None) -> dict:
        url = self.base_url + path
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url, data=data, timeout=self.timeout, headers=self.headers
            ) as response:
                return await self._handle_response(response)

    async def delete(self, path: str, data: dict = None) -> dict:
        url = self.base_url + path
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url, data=data, timeout=self.timeout, headers=self.headers
            ) as response:
                return await self._handle_response(response)

    async def patch(self, path: str, data: dict = None) -> dict:
        url = self.base_url + path
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                url, data=data, timeout=self.timeout, headers=self.headers
            ) as response:
                return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse) -> dict:
        response.raise_for_status()
        return await response.json()
