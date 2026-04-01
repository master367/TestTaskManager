import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Fix psycopg2 UnicodeDecodeError on Windows with non-ASCII system locales
os.environ.setdefault("PGCLIENTENCODING", "UTF8")

from app.database import Base          # import Base so target_metadata is populated
from app.models import User, Task      # noqa: F401  — ensure models are registered
from app.config import settings        # application settings (.env)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

db_url = settings.database_url.replace("+asyncpg", "+psycopg")
# When running Alembic on the host (not inside Docker), the Docker service
# hostname "db" is unreachable.  Fall back to localhost so migrations work
# during local development.
if os.getenv("ALEMBIC_DOCKER") is None:
    db_url = db_url.replace("@db:5432", "@127.0.0.1:5433")
    db_url = db_url.replace("@db:", "@127.0.0.1:5433/")
# Append client_encoding to prevent psycopg2 UnicodeDecodeError on Windows
# with non-ASCII system locales (e.g. Russian).
separator = "&" if "?" in db_url else "?"
db_url = f"{db_url}{separator}client_encoding=utf8"
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = config.attributes.get("connection", None)

    if connectable is None:
        from sqlalchemy import create_engine
        connectable = create_engine(
            config.get_main_option("sqlalchemy.url") or "",
            poolclass=pool.NullPool,
            connect_args={"options": "-c client_encoding=utf8"},
        )

    from sqlalchemy import engine
    if isinstance(connectable, engine.Connection):
        context.configure(
            connection=connectable, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
    else:
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )
            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
