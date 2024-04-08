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


@router.callback_query(F.data == "order_review")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text.order_message_1)
    await state.set_state(Order.business_niche)


@router.message(Order.business_niche)
async def floor(msg: types.Message, state: FSMContext):
    business_niche = msg.text
    await state.update_data(business_niche=business_niche)
    await msg.answer(text.order_message_2)
    await state.set_state(Order.city)


@router.message(Order.city)
async def floor(msg: types.Message, state: FSMContext):
    city = msg.text
    await state.update_data(city=city)
    await msg.answer(text.order_message_3)
    await state.set_state(Order.platforms)


@router.message(Order.platforms)
async def floor(msg: types.Message, state: FSMContext):
    platforms = msg.text
    await state.update_data(platforms=platforms)
    await msg.answer(text.order_message_4, reply_markup=order)
    await state.set_state(Order.expertise_level)


async def process_profile(msg: types.Message, state: FSMContext, expertise_level: str):
    try:
        await state.update_data(expertise_level=expertise_level)
        username = msg.from_user.username
        username_db = db.get_user_id_by_username(username)
        result = await state.get_data()
        db.insert_profile_data(username_db,username, result['business_niche'], result['city'],result['platforms'],result['expertise_level'])
        await msg.answer("Ваш заказ на отзыв успешно добавлен!.", reply_markup=await get_start_keyboard())
        await state.clear()
    except Exception as e:
        await state.clear()
        await msg.answer(f"Произошла ошибка: {e}. Повторите создание анкеты.")


@router.message(F.text == "Высокий")
async def show_business_owner_info(msg: types.Message, state: FSMContext):
    await process_profile(msg, state, "Владелец бизнеса")


@router.message(F.text == "Любой")
async def show_employee_info(msg: types.Message, state: FSMContext):
    await process_profile(msg, state, "Сотрудник")
