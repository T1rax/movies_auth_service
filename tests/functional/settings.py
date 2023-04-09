from pydantic import BaseSettings, Field

class ServiceNotReady(Exception):
    "Raised when service is not awailable yet"
    pass


class TestSettings(BaseSettings):

    cache_host: str = Field('127.0.0.1', env='API_CACHE__HOST')
    cache_port: str = Field('6379', env='API_CACHE__PORT')
    service_url: str =Field('http://127.0.0.1:8000', env='SERVICE_ADDRESS')