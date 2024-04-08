from aiogram import types


async def back_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Вернуться в меню",
                callback_data="back_menu"
            )
        ]]
    )