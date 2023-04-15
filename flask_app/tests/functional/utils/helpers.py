import backoff

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
    
    def ping(self):
        pass
    

class AiohttpHelper:
    def __init__(self, aiohttp_session, test_config):
        self.session = aiohttp_session
    
    async def make_get_request(self, url, path, params=None):
        response = await self.session.get(url+path, json=params)

        try:
            body_json = await response.json()
        except:
            body_json = None

        try:
            body_text = await response.text()
        except:
            body_text = None
    

        return response, body_json, body_text


class DbHelper:
    def __init__(self, db_client, model, app, test_config):
        self.client = db_client
        self.model = model
        self.app = app

    def ping(self):
        pass
    
    def get_user_data(self):
        pass

    def clear_db(self):
        # with self.app.app_context():
        #     deleted = self.model.query.delete()
        #     print('Deleted rows '+str(deleted))

        with self.app.app_context():
            self.client.session.query(self.model).delete()
            self.client.session.commit()