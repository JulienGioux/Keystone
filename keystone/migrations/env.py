import asyncio, sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.keystone.core.db import Base
from src.keystone.models import tenant, role, user
config = context.config
if config.config_file_name is not None: fileConfig(config.config_file_name)
target_metadata = Base.metadata
def run_migrations_offline() -> None:
    db_url = context.get_x_argument(as_dictionary=True).get('db_url')
    url = db_url or config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction(): context.run_migrations()
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction(): context.run_migrations()
async def run_async_migrations() -> None:
    db_url = context.get_x_argument(as_dictionary=True).get('db_url')
    if db_url: config.set_main_option("sqlalchemy.url", db_url)
    connectable = async_engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection: await connection.run_sync(do_run_migrations)
    await connectable.dispose()
def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())
if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()
