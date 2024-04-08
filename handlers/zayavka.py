from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

import text
from keyboards.inline.start import get_start_keyboard
from keyboards.inline.back import back_keyboard
from keyboards.inline.floor import order
from aiogram import F
from aiogram.fsm.context import FSMContext
from state.state import UserState, Order
from bd import Db

router = Router()
db = Db()


@router.callback_query(F.data == "zayavka")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    username = callback.from_user.username
    city = db.get_city_by_username(username)
    try:
        result = db.get_similar_profiles_by_city(city)
        if result is not None:
            formatted_result = "\n\n\n".join([
                                                  f"<b>Пользователь:</b> @{row[2]}\n<b>Бизнес ниша:</b> {row[3]}\n<b>Город:</b> {row[4]}\n<b>Платформа:</b> {row[5]}\n<b>Уровень экспертности:</b> {row[6]}"
                                                 for row in result])
            await callback.message.answer(formatted_result, reply_markup=await get_start_keyboard(), parse_mode="HTML")
        else:
            await callback.message.answer("Поблизости нет активных заявок!")
    except Exception as e:
        print(f"An error occurred: {e}")
