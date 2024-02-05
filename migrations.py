import psycopg2
from psycopg2.extensions import connection
from psycopg2.errors import DuplicateDatabase, DuplicateTable

from config import Postgres


class Queries:
    patients = """
CREATE TABLE Patients (
    telegram_id INTEGER PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    phone CHAR(12) NOT NULL,
    policy VARCHAR(20) NOT NULL,
    passport CHAR(11) NOT NULL
);
    """

    specialties = """
CREATE TABLE Specialties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
    """

    doctors = """
CREATE TABLE Doctors (
    id SERIAL PRIMARY KEY,
    specialist_id INT REFERENCES Specialties (id),
    fullname VARCHAR(255),
    experience INT,
    birthday DATE,
    gender VARCHAR(7),
    email VARCHAR(255)
);
    """

    records = """
CREATE TABLE Records (
    id SERIAL PRIMARY KEY,
    telegram_id INT REFERENCES Patients (telegram_id),
    doctor_id INT REFERENCES Doctors (id),
    date DATE,
    time TIME
);
    """

    all = {
        "Patients": patients,
        "Specialties": specialties,
        "Doctors": doctors,
        "Records": records
    }


def create_db(db_name: str) -> None:
    default_conn = psycopg2.connect(
        host=Postgres.host,
        database="postgres",
        user=Postgres.user,
        password=Postgres.password
    )
    default_conn.autocommit = True

    cursor = default_conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {db_name};")
        print("Database was created")
    except DuplicateDatabase:
        print(f"Database {db_name} already exists!")

    cursor.close()
    default_conn.close()


def create_tables(conn: connection) -> None:
    cursor = conn.cursor()
    conn.autocommit = True

    for table_name, sql in Queries.all.items():
        try:
            cursor.execute(sql)
            print(f"Table {table_name} created")
        except DuplicateTable:
            print(f"Table {table_name} already exists!")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    # Создание БД clinic
    create_db(db_name="clinic")

    # Создание таблиц
    CLINIC_DB_CONN = psycopg2.connect(
        host=Postgres.host,
        database=Postgres.database,
        user=Postgres.user,
        password=Postgres.password
    )

    create_tables(conn=CLINIC_DB_CONN)
