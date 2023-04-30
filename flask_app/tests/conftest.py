# Imports for local testing
import sys

sys.path.insert(0, "/home/tirax/movies_auth_service/flask_app")
sys.path.insert(0, "/home/tirax/movies_auth_service/tests")


pytest_plugins = (
    "fixtures.asyncio",
    "fixtures.db",
    "fixtures.mds",
    "fixtures.aiohttp",
    "fixtures.unit",
)
