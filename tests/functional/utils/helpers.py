import backoff

from elasticsearch.helpers import async_bulk

class NoResultsEsception(Exception):
    "Raised when service return empty results"
    pass
        

class MdsHelper:
    def __init__(self, cache_client, test_config):
        self.cache_client = cache_client

    
    async def clear_all(self):
        await self.cache_client.flushall()
        
    async def get_value(self, key):
        return await self.cache_client.get(key)
    

class AiohttpHelper:
    def __init__(self, aiohttp_session, test_config):
        self.session = aiohttp_session
    
    async def make_get_request(self, url, path, params=None):
        async with self.session.get(url+path, params=params) as response:
            body = await response.json()
            headers = response.headers
            status = response.status

        if isinstance(body, list):
            length = len(body)
        else:
            length = 0

        return status, length, body, headers
