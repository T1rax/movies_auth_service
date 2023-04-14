import backoff
import logging
import os, sys

from flask_app.database.db import db
from redis import Redis

parent = os.path.abspath('.')
sys.path.insert(1, parent)
from settings import test_settings, ServiceNotReady

logging.getLogger('elastic_transport').setLevel(logging.ERROR)


@backoff.on_exception(backoff.expo, ServiceNotReady, jitter=backoff.full_jitter, max_time=180)
def wait_for_mds():
    cache_client = Redis(host=test_settings.cache_host, port=test_settings.cache_port)
    
    if not cache_client.ping():
        logging.info('Redis not awailable yet, wait for next try')
        raise ServiceNotReady('Redis not awailable yet')
    

@backoff.on_exception(backoff.expo, ServiceNotReady, jitter=backoff.full_jitter, max_time=180)
def wait_for_db():
    cache_client = Redis(host=test_settings.cache_host, port=test_settings.cache_port)
    
    if not cache_client.ping():
        logging.info('Redis not awailable yet, wait for next try')
        raise ServiceNotReady('Redis not awailable yet')


if __name__ == '__main__':
    wait_for_mds()
    wait_for_db()