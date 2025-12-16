import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def make_engine():
    """
    Creates a SQLAlchemy engine for Azure Postgres.
    Uses sslmode=require by default.
    """
    load_dotenv()

    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT", "5432")
    db   = os.getenv("PGDATABASE", "postgres")
    user = os.getenv("PGUSER")
    pw   = os.getenv("PGPASSWORD")
    ssl  = os.getenv("PGSSLMODE", "require")

    if not all([host, port, db, user, pw]):
        raise ValueError("Missing one or more required env vars: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD")

    # Quote password in case it has special characters
    pw_safe = quote_plus(pw)

    url = f"postgresql+psycopg2://{user}:{pw_safe}@{host}:{port}/{db}?sslmode={ssl}"
    engine = create_engine(url, pool_pre_ping=True)
    return engine


def test_connection(engine):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1;"))


def read_sql_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
