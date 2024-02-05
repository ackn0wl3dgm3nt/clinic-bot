from aiogram.fsm.state import StatesGroup, State


class ToMainMenu(StatesGroup):
    button = State()


class MainMenu(StatesGroup):
    menu = State()


# class Info(StatesGroup):
#     text = State()


class Register(StatesGroup):
    fullname = State()
    birthday = State()
    phone = State()
    policy = State()
    passport = State()
    check = State()


class DoctorRecord(StatesGroup):
    specialist = State()
    doctor = State()
    date = State()
    time = State()
    check = State()
