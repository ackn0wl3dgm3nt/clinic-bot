import psycopg2
from psycopg2.errors import DuplicateDatabase, DuplicateTable

from config import Postgres


class Queries:
    create_db = "CREATE DATABASE {};"

    patients_table = """
CREATE TABLE Patients (
    telegram_id INTEGER PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    phone CHAR(12) NOT NULL,
    policy VARCHAR(20) NOT NULL,
    passport CHAR(11) NOT NULL
);
    """

    specialties_table = """
CREATE TABLE Specialties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
    """

    doctors_table = """
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

    records_table = """
CREATE TABLE Records (
    id SERIAL PRIMARY KEY,
    telegram_id INT REFERENCES Patients (telegram_id),
    doctor_id INT REFERENCES Doctors (id),
    date DATE,
    time TIME
);
    """

    specialties_filling = """
INSERT INTO Specialties (name)
VALUES ('Хирург'),
('Терапевт'),
('Стоматолог'),
('Уролог'),
('Гинеколог'),
('Нарколог'),
('Психиатр'),                  
('Дерматолог'),                                                                                          
('Отоларинголог'),                      
('Эндокринолог');
    """

    doctors_filling = """
INSERT INTO Doctors (specialist_id, fullname, experience, birthday, gender, email)
VALUES 
    (1, 'Смелов Владимир Владиславович', 15, '1983-09-23', 'Мужской', 'smelov.v@mail.ru'),
    (2, 'Акунович Станислав Иванович', 20, '1991-03-17', 'Мужской', 'stan@mail.ru'),
    (3, 'Колесников Виталий Леонидович', 3, '1992-03-28', 'Мужской', 'Kolesnikov@mail.ru'),
    (4, 'Бракович Андрей Игоревич', 12, '1987-10-17', 'Мужской', 'brakovich@gmail.ru'),
    (2, 'Дятко Александр Аркадьевич', 10, '1993-02-24', 'Мужской', 'alex.dyatko@mail.ru'),
    (5, 'Урбанович Павел Павлович', 8, '1994-04-16', 'Мужской', 'urban.pavel@mail.ru'),
    (6, 'Гурин Николай Иванович', 9, '1996-06-18', 'Мужской', 'gyrin@mail.ru'),
    (7, 'Жиляк Надежда Александровна', 16, '1982-04-25', 'Женщина', 'zhilyak@gmail.ru'),                  
    (8, 'Мороз Елена Станиславовна', 7, '1996-08-14', 'Женщина', 'elena.morozova@mail.ru'),                                                                                          
    (9, 'Барташевич Святослав Александрович', 25, '1997-11-27', 'Мужской', 'bartash@gmail.ru'),
    (3, 'Арсентьев Виталий Арсентьевич', 19, '1982-04-23', 'Мужской', 'ars.vitali@mail.ru'),                      
    (10, 'Барановский Станислав Иванович', 2, '1991-07-19', 'Мужской', 'baran@mail.ru'),
    (1, 'Насковец Михаил Трофимович', 17, '1984-02-28', 'Мужской', 'mih.trofimovich@gmail.ru');
    """

    tables = {
        "Patients": patients_table,
        "Specialties": specialties_table,
        "Doctors": doctors_table,
        "Records": records_table
    }

    filling = {
        "Specialties": specialties_filling,
        "Doctors": doctors_filling
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
        cursor.execute(Queries.create_db.format(db_name))
        print("Database was created")
    except DuplicateDatabase:
        print(f"Database {db_name} already exists!")

    cursor.close()
    default_conn.close()


def create_tables() -> None:
    conn = Postgres.get_conn()

    cursor = conn.cursor()
    conn.autocommit = True

    for table_name, sql in Queries.tables.items():
        try:
            cursor.execute(sql)
            print(f"Table {table_name} created")
        except DuplicateTable:
            print(f"Table {table_name} already exists!")

    cursor.close()


def fill_tables() -> None:
    conn = Postgres.get_conn()

    cursor = conn.cursor()
    conn.autocommit = True

    for table_name, sql in Queries.filling.items():
        try:
            cursor.execute(sql)
            print(f"Table {table_name} filled")
        except Exception as error:
            print(error)

    cursor.close()


def run_migrate() -> None:
    steps = [
        lambda: create_db(db_name=Postgres.database),
        lambda: create_tables(),
        lambda: fill_tables()
    ]

    for step in steps:
        step()


if __name__ == "__main__":
    run_migrate()
    print("\nMigrations is completed!")
