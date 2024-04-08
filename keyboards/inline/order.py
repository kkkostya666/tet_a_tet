from aiogram import types


async def get_order_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Создать анкету",
                callback_data="create_new"
            ),
            types.InlineKeyboardButton(
                text="Удалить анкету",
                callback_data="create_delete"
            ),
            types.InlineKeyboardButton(
                text='Редактировать анкету',
                callback_data='create_edit'
            ),
        ]]
    )


async def get_delete_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Да",
                callback_data="da"
            ),
            types.InlineKeyboardButton(
                text="Нет",
                callback_data="net"
            ),
        ]]
    )