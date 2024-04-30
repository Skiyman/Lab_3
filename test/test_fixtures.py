import pytest
from alembic.command import upgrade
from httpx import AsyncClient, ASGITransport

import config
from db import use_temp_database, get_alembic_config, set_db_url


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio", {"use_uvloop": True}


@pytest.fixture(scope="session")
async def temp_db():
    async with use_temp_database(config.POSTGRES_URL) as temp_db_url:
        yield temp_db_url


@pytest.fixture(scope="session")
def alembic_config(temp_db):
    yield get_alembic_config(temp_db)


@pytest.fixture(scope="session")
async def migrated_temp_db(alembic_config):
    upgrade(alembic_config, "head")
    yield alembic_config.get_main_option("sqlalchemy.url")


@pytest.fixture(scope="session")
def test_db(migrated_temp_db):
    set_db_url(migrated_temp_db)


@pytest.fixture()
def app(test_db):
    from main import app
    yield app


@pytest.fixture()
async def client(app):
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client