import os

import psycopg2
from psycopg2.extensions import connection
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

class Postgres:
    host = os.getenv("POSTGRES_HOST")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    @staticmethod
    def get_conn() -> connection:
        conn = psycopg2.connect(
            host=Postgres.host,
            database=Postgres.database,
            user=Postgres.user,
            password=Postgres.password
        )
        conn.autocommit = True
        return conn

    @staticmethod
    def close_conn(conn: connection):
        conn.close()


BOT_TOKEN = os.getenv("BOT_TOKEN")
STORAGE = MemoryStorage()
