from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    username = State()
    sity = State()
    floor = State()
    age = State()
    experience = State()
    sites = State()
    mood = State()
    otziv = State()
    level = State()
    info_user = State()


class Order(StatesGroup):
    user_id = State()
    business_niche = State()
    city = State()
    platforms = State()
    expertise_level = State()