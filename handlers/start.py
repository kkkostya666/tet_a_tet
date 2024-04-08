from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart
from keyboards.inline.start import get_start_keyboard
import text
from aiogram import F
router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text=text.start_text,
                         reply_markup=await get_start_keyboard())

