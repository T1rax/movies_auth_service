# python shell
import redis
from flask_app.database.db import redis_db


'''
Для хранения данных в базе можно использовать userId_operation в качестве ключа 
— это как раз уникальная строка в базе. 
В качестве значения можно хранить сам токен. 
Для этого достаточно пары простых команд:
'''
redis_db.get('key')  # Получить значение по ключу
redis_db.set('key', 'value')  # Положить значение по ключу
redis_db.expire('key', 10)  # Установить время жизни ключа в секундах
# А можно последние две операции сделать за один запрос к Redis.
redis_db.setex('key', 10, 'value')  # Положить значение по ключу с ограничением времени жизни в секундах


'''
Также можно атомарно работать с множеством ключей, например, для массового сброса сессий. 
Или когда в нескольких атомарных операциях произошёл сбой: 
сеть моргнула, маршрутизация багнула, кластер был недоступен. 
На такой случай можно использовать pipeline, как в транзакции в PostgreSQL.
'''
pipeline = redis_db.pipeline()
pipeline.setex('key', 10, 'value')
pipeline.setex('key2', 10, 'value')
pipeline.execute() 


'''
Здесь всего две операции для транзакции, но их бывает намного больше. 
Чтобы сократить этот код, в redis-py есть специальная функция. 

Установите сразу множество ключей:
'''
def set_two_factor_auth_code(pipeline: redis.client.Pipeline) -> None:
    pipeline.setex('key', 10, 'value')
    pipeline.setex('key2', 10, 'value')
    pipeline.setex('key3', 10, 'value')
    pipeline.setex('key4', 10, 'value')

redis_db.transaction(set_two_factor_auth_code) 