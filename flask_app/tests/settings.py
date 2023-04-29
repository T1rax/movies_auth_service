from pydantic import BaseSettings, Field

class ServiceNotReady(Exception):
    "Raised when service is not awailable yet"
    pass


class TestSettings(BaseSettings):

    mds_host: str = Field('redis', env='AUTH_MDS__HOST')
    mds_port: str = Field('6379', env='AUTH_MDS__PORT')
    service_url: str =Field('http://127.0.0.1:5000', env='AUTH_SERVICE__URL')

test_settings = TestSettings()