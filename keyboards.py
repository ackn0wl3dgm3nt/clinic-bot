from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from wordings import *


class MainMenuKeyboards:
    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        kb = [
            [KeyboardButton(text=w_info)],
            [KeyboardButton(text=w_reg)],
            [KeyboardButton(text=w_record)],
        ]

        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def to_main_menu() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=w_to_mm)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )


class RegistrationKeyboards:
    @staticmethod
    def confirm_registration() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=w_reg_ok), KeyboardButton(text=w_reg_again)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )


class RecordKeyboards:
    @staticmethod
    def specialties(specialties: list) -> ReplyKeyboardMarkup:
        keyboard = []
        for specialist in specialties:
            keyboard.append(
                [KeyboardButton(text=specialist)]
            )
        keyboard.append([KeyboardButton(text=w_to_mm)])

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )

    @staticmethod
    def doctors(doctors: list) -> ReplyKeyboardMarkup:
        keyboard = []

        for doctor in doctors:
            keyboard.append(
                [KeyboardButton(text=doctor)]
            )
        keyboard.append([KeyboardButton(text=w_to_mm)])

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
