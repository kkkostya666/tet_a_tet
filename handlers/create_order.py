from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardRemove

import text
from keyboards.inline.start import get_start_keyboard
from keyboards.inline.back import back_keyboard
from keyboards.inline.floor import keyboard, mood, user_info
from keyboards.inline.order import get_order_keyboard, get_delete_keyboard
from aiogram import F
from aiogram.fsm.context import FSMContext
from state.state import UserState
from bd import Db

router = Router()
db = Db()


@router.callback_query(F.data == "back_menu")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text.clear_anketa,
                                  reply_markup=await get_start_keyboard())


@router.callback_query(F.data == "order_create")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.new_order1,reply_markup=await get_order_keyboard())


@router.callback_query(F.data == "create_new")
async def create_order(callback: types.CallbackQuery, state: FSMContext):
    username = callback.from_user.username
    if db.check_username_exists(username) == 0:
        await state.set_state(UserState.sity)
        await callback.message.answer(text.info_create)
        await callback.message.answer(text.sity, reply_markup=await back_keyboard())
        await callback.message.delete()
    else:
        await callback.message.answer(text.error)


@router.callback_query(F.data == "create_delete")
async def create_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Вы действительно хотите удалить свою анкету?",reply_markup=await get_delete_keyboard())


@router.callback_query(F.data == "da")
async def create_delete(callback: types.CallbackQuery, state: FSMContext):
    username = callback.from_user.username
    try:
        result = db.delete_user_by_username(username)
        await callback.message.answer(text=f"Ваша анкета {username} успешно удалена",reply_markup=await get_start_keyboard())
    except ValueError:
        await callback.message.answer(text='У вас нет анкеты')
        return


@router.callback_query(F.data == "net")
async def create_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Вы вернулись в главное меню!", reply_markup=await get_start_keyboard())


@router.message(UserState.sity)
async def floor(msg: types.Message, state: FSMContext):
    sity = msg.text
    await state.update_data(sity=sity)
    await msg.answer(text.floor, reply_markup=keyboard)
    await state.set_state(UserState.floor)


@router.message(F.text == "Мужской")
async def show_info(msg: types.Message, state: FSMContext):
    await state.update_data(floor="Мужской")
    await state.set_state(UserState.age)
    await msg.answer(text.age, reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Женский")
async def show_info(msg: types.Message, state: FSMContext):
    await state.update_data(floor="Женский")
    await state.set_state(UserState.age)
    await msg.answer(text.age,reply_markup=ReplyKeyboardRemove())


@router.message(UserState.age)
async def floor(msg: types.Message, state: FSMContext):
    try:
        age = int(msg.text)
    except ValueError:
        await msg.answer("Введите числовое значение!")
        return
    await state.update_data(age=age)
    await msg.answer(text.experience)
    await state.set_state(UserState.experience)


@router.message(UserState.experience)
async def floor(msg: types.Message, state: FSMContext):
    experience = msg.text
    await state.update_data(experience=experience)
    await msg.answer(text.sites)
    await state.set_state(UserState.sites)


@router.message(UserState.sites)
async def floor(msg: types.Message, state: FSMContext):
    sites = msg.text
    await state.update_data(sites=sites)
    await msg.answer(text.mood, reply_markup=mood)
    await state.set_state(UserState.mood)


@router.message(F.text == "Позитивный")
async def show_info(msg: types.Message, state: FSMContext):
    await state.update_data(mood="Позитивный")
    await state.set_state(UserState.otziv)
    await msg.answer(text.otziv, reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Негативный")
async def show_info(msg: types.Message, state: FSMContext):
    await state.update_data(mood="Негативный")
    await state.set_state(UserState.otziv)
    await msg.answer(text.otziv, reply_markup=ReplyKeyboardRemove())


@router.message(UserState.otziv)
async def floor(msg: types.Message, state: FSMContext):
    otziv = msg.text
    await state.update_data(otziv=otziv)
    await msg.answer(text='Как Вы оцениваете свой уровень экспертности в написании отзывов, по шкале от 1 до 5?')
    await state.set_state(UserState.level)


@router.message(UserState.level)
async def floor(msg: types.Message, state: FSMContext):
    level = msg.text
    if not level.isdigit() or not (1 <= int(level) <= 5):
        await msg.answer("Пожалуйста, введите число от 1 до 5.")
        return  # Прерываем выполнение обработчика
    await state.update_data(level=level)
    await msg.answer(text.info_user, reply_markup=user_info)
    await state.set_state(UserState.info_user)


async def process_profile(msg: types.Message, state: FSMContext, info_user: str):
    try:
        await state.update_data(info_user=info_user)
        result = await state.get_data()
        username = msg.from_user.username
        db.user_add(username, result['sity'], result['age'], result['experience'], result['sites'], result['mood'],
                    result['otziv'], result['level'],
                    result['info_user'])
        await msg.answer("Ваша анкета успешно добавлена!.", reply_markup=await get_start_keyboard())
        await state.clear()
    except Exception as e:
        await msg.answer(f"Произошла ошибка: {e}. Повторите создание анкеты.")


@router.message(F.text == "Владелец бизнеса")
async def show_business_owner_info(msg: types.Message, state: FSMContext):
    await process_profile(msg, state, "Владелец бизнеса")


@router.message(F.text == "Сотрудник")
async def show_employee_info(msg: types.Message, state: FSMContext):
    await process_profile(msg, state, "Сотрудник")


@router.message(F.text == "Фрилансер")
async def show_freelancer_info(msg: types.Message, state: FSMContext):
    await process_profile(msg, state, "Фрилансер")