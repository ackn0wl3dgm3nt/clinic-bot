from config import Postgres
from functools import wraps
from psycopg2.extensions import cursor

DB_CONN = Postgres.get_conn()


def get_cursor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cursor = DB_CONN.cursor()
        try:
            result = func(cursor, *args, **kwargs)
        finally:
            cursor.close()
        return result
    return wrapper


class PatientRepository:
    @staticmethod
    @get_cursor
    def create_patient(
            cursor: cursor,
            telegram_id: int, fullname: str, birthday: str, phone: str, policy: str, passport: str
    ) -> None:
        sql = """INSERT INTO Patients (telegram_id, fullname, birthday, phone, policy, passport) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (telegram_id, fullname, birthday, phone, policy, passport)
        cursor.execute(sql, params)

    @staticmethod
    @get_cursor
    def check_patient(
            cursor: cursor, telegram_id: int
    ) -> bool:
        sql = "SELECT COUNT(*) FROM Patients WHERE telegram_id = %s"
        cursor.execute(sql, (telegram_id,))
        result = cursor.fetchone()[0]
        return result > 0


class SpecialistsRepository:
    @staticmethod
    @get_cursor
    def get_all(cursor: cursor) -> list:
        sql = "SELECT name FROM Specialties"
        cursor.execute(sql)
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    @get_cursor
    def get_id_by_name(cursor: cursor, name: str) -> int:
        sql = "SELECT id FROM Specialties WHERE name=%s"
        cursor.execute(sql, (name,))
        return int(cursor.fetchone()[0])


class DoctorRepository:
    @staticmethod
    @get_cursor
    def get_all_fullnames(cursor: cursor) -> list:
        sql = "SELECT fullname FROM Doctors"
        cursor.execute(sql)
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    @get_cursor
    def get_all_by_spec(cursor: cursor, specialist_id: int) -> list:
        sql = "SELECT fullname FROM Doctors WHERE specialist_id=%s "
        cursor.execute(sql, (specialist_id,))
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    @get_cursor
    def get_id_by_fullname(cursor: cursor, fullname: str) -> int:
        sql = "SELECT id FROM Doctors WHERE fullname=%s"
        cursor.execute(sql, (fullname,))
        return int(cursor.fetchone()[0])


class RecordRepository:
    @staticmethod
    @get_cursor
    def create_record(
            cursor: cursor,
            telegram_id: int,
            doctor_id: int,
            date: str,
            time: str
    ) -> None:
        sql = "INSERT INTO Records (telegram_id, doctor_id, date, time) VALUES (%s, %s, %s, %s)"
        params = (telegram_id, doctor_id, date, time)

        cursor.execute(sql, params)
