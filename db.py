import os.path
import uuid
from contextlib import asynccontextmanager

import sqlalchemy
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import POSTGRES_URL


class _DbConfig:
    url = POSTGRES_URL


@asynccontextmanager
async def make_session():
    engine = create_async_engine(_DbConfig.url)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    await engine.dispose()


def set_db_url(url: str):
    _DbConfig.url = url


def get_alembic_config(db_url: str = POSTGRES_URL) -> AlembicConfig:
    config = AlembicConfig(
        file_="alembic.ini",
    )
    config.set_main_option('sqlalchemy.url', db_url)
    return config


def run_migrations() -> None:
    alembic_cfg = get_alembic_config(POSTGRES_URL)
    command.upgrade(alembic_cfg, 'head')


@asynccontextmanager
async def use_temp_database(source_db_url: str):
    temp_db_name = f"test_db_{uuid.uuid4().hex}"
    temp_db_url = f"{os.path.dirname(source_db_url)}/{temp_db_name}"

    await _create_database_async(source_db_url, temp_db_name)
    try:
        yield temp_db_url
    finally:
        await _drop_database_async(source_db_url, temp_db_name)


async def _create_database_async(url, database_name: str):
    connect_url = f"{os.path.dirname(url)}/postgres"
    db_engine = create_async_engine(connect_url, isolation_level="AUTOCOMMIT")
    async with db_engine.begin() as conn:
        text = "CREATE DATABASE {}".format(database_name.replace("'", "\\'"))
        await conn.execute(sqlalchemy.text(text))


async def _drop_database_async(url, database_name: str):
    connect_url = f"{os.path.dirname(url)}/postgres"
    db_engine = create_async_engine(connect_url, isolation_level="AUTOCOMMIT")
    async with db_engine.begin() as conn:
        text = "DROP DATABASE {}".format(database_name.replace("'", "\\'"))
        await conn.execute(sqlalchemy.text(text))
