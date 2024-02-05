import datetime
from db import *


class RegisterValidator:
    @staticmethod
    def check_fullname(full_name: str) -> bool:
        return len(full_name.split(" ")) == 3

    @staticmethod
    def check_birthday(birthday: str) -> bool:
        try:
            d = datetime.datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def check_phone(phone_number: str) -> bool:
        return phone_number.startswith("+7") and len(phone_number) == 12 and phone_number[2:].isdigit()

    @staticmethod
    def check_policy(policy_number: str) -> bool:
        try:
            number = int(policy_number)
            return len(policy_number) == 16
        except ValueError:
            return False

    @staticmethod
    def check_passport(password_number: str) -> bool:
        try:
            password_number = password_number.split(" ")
            series = password_number[0]
            number = password_number[1]
            return len(series) == 4 and len(number) == 6
        except IndexError:
            return False


class RecordValidator:
    @staticmethod
    def check_is_specialist(name) -> bool:
        specialties = Specialists.get_all()
        return name in specialties

    @staticmethod
    def check_is_doctor(fullname: str) -> bool:
        doctors = Doctor.get_all_fullnames()
        return fullname in doctors

    @staticmethod
    def check_date(input_date: str) -> bool:
        date = datetime.datetime.strptime(input_date, "%d.%m.%Y")
        if date.weekday() in [5, 6]:  # Воскресенье
            return False
        else:
            return True

    @staticmethod
    def check_time(input_time) -> bool:
        time = datetime.datetime.strptime(input_time, "%H:%M")
        if time.hour < 8 or time.hour > 20:
            return False
        else:
            return True
