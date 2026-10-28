# async_client.py
import httpx
import pprint

class AsyncPetstoreClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def close(self):
        await self.client.aclose()

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        response = await self.client.request(method, url, **kwargs)

        pprint.pprint(f'{method} example')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.text)
        pprint.pprint('**********')
        
        return response

    async def get(self, endpoint: str, **kwargs):
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs):
        return await self._request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs):
        return await self._request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        return await self._request("DELETE", endpoint, **kwargs)