import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from config import *
from keyboards import *
from states import *
from validators import *

dp = Dispatcher(storage=STORAGE)


# Главное меню
@dp.message(Command("start"))
@dp.message(F.text == w_to_mm)
async def start(message: types.Message, state: FSMContext):
    await state.set_state(MainMenu.menu)
    await message.answer(text=w_mm, reply_markup=MainMenuKeyboards.main_menu())


# Информация
@dp.message(F.text == w_info, MainMenu.menu)
async def info(message: types.Message, state: FSMContext):
    await state.set_state(ToMainMenu.button)
    await message.answer(text=w_info_text, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=MainMenuKeyboards.to_main_menu())


# Регистрация
@dp.message(F.text == w_reg, MainMenu.menu)
async def register_fullname(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if PatientRepository.check_patient(telegram_id=user_id):
        await message.answer(w_user_exists)
        await start(message, state)
        return

    await state.set_state(Register.fullname)
    await message.answer(w_input_fullname, reply_markup=MainMenuKeyboards.to_main_menu())


@dp.message(Register.fullname)
async def register_birthday(message: types.Message, state: FSMContext):
    fullname = message.text
    if not RegisterValidator.check_fullname(fullname):
        await message.answer(w_incorrect_fullname, reply_markup=MainMenuKeyboards.to_main_menu())
        return

    await state.update_data(full_name=fullname)
    await state.set_state(Register.birthday)
    await message.answer(w_input_birthday, reply_markup=MainMenuKeyboards.to_main_menu())


@dp.message(Register.birthday)
async def register_phone(message: types.Message, state: FSMContext):
    birthday = message.text
    if not RegisterValidator.check_birthday(birthday):
        await message.answer(w_incorrect_birthday, reply_markup=MainMenuKeyboards.to_main_menu())
        return

    await state.update_data(birthday=birthday)
    await state.set_state(Register.phone)
    await message.answer(w_input_phone, reply_markup=MainMenuKeyboards.to_main_menu())


@dp.message(Register.phone)
async def register_policy(message: types.Message, state: FSMContext):
    phone = message.text
    if not RegisterValidator.check_phone(phone):
        await message.answer(w_incorrect_phone, reply_markup=MainMenuKeyboards.to_main_menu())
        return

    await state.update_data(phone=phone)
    await state.set_state(Register.policy)
    await message.answer(w_input_policy, reply_markup=MainMenuKeyboards.to_main_menu())


@dp.message(Register.policy)
async def register_passport(message: types.Message, state: FSMContext):
    policy = message.text
    if not RegisterValidator.check_policy(policy):
        await message.answer(w_incorrect_policy, reply_markup=MainMenuKeyboards.to_main_menu())
        return

    await state.update_data(policy=policy)
    await state.set_state(Register.passport)
    await message.answer(w_input_passport, reply_markup=MainMenuKeyboards.to_main_menu())


@dp.message(Register.passport)
async def register_check(message: types.Message, state: FSMContext):
    passport = message.text
    if not RegisterValidator.check_passport(passport):
        await message.answer(w_incorrect_passport)
        return
    await state.update_data(passport=passport)

    await message.answer(w_reg_confirm)
    data = await state.get_data()
    await message.answer(text=w_reg_confirm_text.format(
        data["full_name"],
        data["birthday"],
        data["phone"],
        data["policy"],
        data["passport"]
    ), reply_markup=RegistrationKeyboards.confirm_registration())
    await state.set_state(Register.check)


@dp.message(Register.check)
async def register_over(message: types.Message, state: FSMContext):
    action = message.text
    user_id = message.from_user.id
    if action == w_reg_ok:
        data = await state.get_data()
        params = [user_id] + list(data.values())
        PatientRepository.create_patient(*params)

        await message.answer(w_reg_finished)
        await start(message, state)
    else:
        await register_fullname(message, state)


# Запись к врачу
@dp.message(F.text == w_record, MainMenu.menu)
async def choose_record_specialist(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not PatientRepository.check_patient(telegram_id=user_id):
        await message.answer(w_user_not_exists)
        await start(message, state)
        return

    specialties = SpecialistsRepository.get_all()
    await message.answer(w_record_specialist, reply_markup=RecordKeyboards.specialties(specialties))
    await state.set_state(DoctorRecord.specialist)


@dp.message(DoctorRecord.specialist)
async def choose_record_doctor(message: types.Message, state: FSMContext):
    specialist = message.text
    if not RecordValidator.check_is_specialist(specialist):
        await message.answer(w_incorrect_specialist)
        return
    spec_id = SpecialistsRepository.get_id_by_name(name=specialist)
    doctors = DoctorRepository.get_all_by_spec(specialist_id=spec_id)

    await state.update_data(specialist=specialist)
    await message.answer(w_record_doctor, reply_markup=RecordKeyboards.doctors(doctors))
    await state.set_state(DoctorRecord.doctor)


@dp.message(DoctorRecord.doctor)
async def choose_record_date(message: types.Message, state: FSMContext):
    doctor = message.text
    if not RecordValidator.check_is_doctor(doctor):
        await message.answer(w_incorrect_doctor)
        return

    await state.update_data(doctor=doctor)
    await message.answer(w_record_date, reply_markup=MainMenuKeyboards.to_main_menu())
    await state.set_state(DoctorRecord.date)


@dp.message(DoctorRecord.date)
async def choose_record_time(message: types.Message, state: FSMContext):
    date = message.text
    if not RecordValidator.check_date(date):
        await message.answer(w_incorrect_date)
        return

    await state.update_data(date=date)
    await message.answer(w_record_time, reply_markup=MainMenuKeyboards.to_main_menu())
    await state.set_state(DoctorRecord.time)


@dp.message(DoctorRecord.time)
async def check_record(message: types.Message, state: FSMContext):
    time = message.text
    if not RecordValidator.check_time(time):
        await message.answer(w_incorrect_time)
        return

    await state.update_data(time=time)
    data = await state.get_data()

    RecordRepository.create_record(
        telegram_id=message.from_user.id,
        doctor_id=DoctorRepository.get_id_by_fullname(data.get("doctor")),
        date=data.get("date"),
        time=data.get("time")
    )

    await message.answer(w_record_finished)
    await start(message, state)


# Запуск бота
async def main():
    try:
        logging.basicConfig(level=logging.INFO)
        bot = Bot(token=BOT_TOKEN)
        await dp.start_polling(bot)
    except:
        Postgres.close_conn(DB_CONN)


# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
