import psycopg2
from config import Postgres

DB_CONN = psycopg2.connect(
    host=Postgres.host,
    database=Postgres.database,
    user=Postgres.user,
    password=Postgres.password
)


class Patient:
    @staticmethod
    def create(
            telegram_id: int, fullname: str, birthday: str,
            phone: str, policy: str, passport: str
    ) -> None:
        cursor = DB_CONN.cursor()
        sql = """INSERT INTO Patients (telegram_id, fullname, birthday, phone, policy, passport) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (telegram_id, fullname, birthday, phone, policy, passport)

        cursor.execute(sql, params)
        DB_CONN.commit()
        cursor.close()

    @staticmethod
    def check(
            telegram_id: int
    ) -> bool:
        cursor = DB_CONN.cursor()
        sql = "SELECT COUNT(*) FROM Patients WHERE telegram_id = %s"
        cursor.execute(sql, (telegram_id,))
        result = cursor.fetchone()[0]
        cursor.close()

        return result > 0


class Specialists:
    @staticmethod
    def get_all() -> list:
        cursor = DB_CONN.cursor()
        sql = "SELECT name FROM Specialties"
        cursor.execute(sql)
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_id_by_name(name: str) -> int:
        cursor = DB_CONN.cursor()
        sql = "SELECT id FROM Specialties WHERE name=%s"
        cursor.execute(sql, (name,))
        return int(cursor.fetchone()[0])


class Doctor:
    @staticmethod
    def get_all_fullnames() -> list:
        cursor = DB_CONN.cursor()
        sql = "SELECT fullname FROM Doctors"
        cursor.execute(sql)
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_all_by_spec(specialist_id: int) -> list:
        cursor = DB_CONN.cursor()
        sql = "SELECT fullname FROM Doctors WHERE specialist_id=%s "
        cursor.execute(sql, (specialist_id,))
        return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_id_by_fullname(fullname: str) -> int:
        cursor = DB_CONN.cursor()
        sql = "SELECT id FROM Doctors WHERE fullname=%s"
        cursor.execute(sql, (fullname,))
        return int(cursor.fetchone()[0])


class Record:
    @staticmethod
    def create(
            telegram_id: int,
            doctor_id: int,
            date: str,
            time: str
    ) -> None:
        cursor = DB_CONN.cursor()
        sql = "INSERT INTO Records (telegram_id, doctor_id, date, time) VALUES (%s, %s, %s, %s)"
        params = (telegram_id, doctor_id, date, time)

        cursor.execute(sql, params)
        DB_CONN.commit()
        cursor.close()


if __name__ == "__main__":
    pass
