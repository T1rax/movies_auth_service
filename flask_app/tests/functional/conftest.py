#Imports for local testing
import sys
sys.path.insert(0, '/home/tirax/movies_auth_service')
sys.path.insert(0, '/home/tirax/movies_auth_service/flask_app')
sys.path.insert(0, '/home/tirax/movies_auth_service/tests/functional')
sys.path.insert(0, '/home/seo/proj/sprint_5/movies_auth_service/tests/functional')


pytest_plugins = (
    'fixtures.asyncio',
    'fixtures.flask',
    'fixtures.mds',
    'fixtures.aiohttp'
    )
