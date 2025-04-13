import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import text
from delivery.infrastructure.Adapters.Postgres.Models.OrderAggregate.order import Base
from delivery.infrastructure.Adapters.Postgres.db import get_url


@pytest_asyncio.fixture
async def db_conn():
    db_url = get_url()
    engine = create_async_engine(
        url=db_url,
        pool_pre_ping=True,
        connect_args={},
    )
    try:
        async with engine.connect() as conn:
            yield conn
    except ConnectionError:
        yield


@pytest_asyncio.fixture
async def exec_db_tests(db_conn) -> bool:
    return bool(db_conn) if db_conn else False


@pytest_asyncio.fixture
async def create_db_schema():
    async def create_schema_exec(db_conn: AsyncConnection, name: str) -> None:
        sql_exec = f"""CREATE SCHEMA IF NOT EXISTS {name}"""
        await db_conn.execute(text(sql_exec))

    return create_schema_exec


@pytest_asyncio.fixture
async def create_tables():
    async def create_table_exec(db_conn: AsyncConnection) -> None:
        await db_conn.run_sync(Base.metadata.drop_all, checkfirst=True)
        await db_conn.run_sync(Base.metadata.create_all, checkfirst=True)

    return create_table_exec


@pytest_asyncio.fixture
async def db_init(exec_db_tests, db_conn, create_db_schema, create_tables):
    if exec_db_tests:
        for tbl in Base.metadata.tables.values():
            await create_db_schema(db_conn=db_conn, name=tbl.schema)
        await create_tables(db_conn=db_conn)
        await db_conn.commit()


@pytest_asyncio.fixture
async def db_rollback(exec_db_tests, db_conn):
    if exec_db_tests:
        for tbl in Base.metadata.tables.values():
            sql_exec = f"""DROP SCHEMA IF EXISTS {tbl.schema} CASCADE"""
            await db_conn.execute(text(sql_exec))
            await db_conn.commit()
