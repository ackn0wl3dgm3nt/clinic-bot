import psycopg2
from aiogram.fsm.storage.memory import MemoryStorage


class Postgres:
    host = "localhost"
    user = "postgres"
    database = "clinic"
    password = "postgres"


BOT_TOKEN = "6744325432:AAG0wFcuxViTQqrS_8pnxRPAb9U6xYjVzkA"
STORAGE = MemoryStorage()
