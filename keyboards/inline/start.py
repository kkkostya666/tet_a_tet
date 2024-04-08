from aiogram import types


async def get_start_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="Моя анкета",
                callback_data="order_create"
            ),
            types.InlineKeyboardButton(
                text="Заказать отзыв",
                callback_data="order_review"
            ),
            types.InlineKeyboardButton(
                text='Мои оценки',
                callback_data='my_grade'
            ),
            types.InlineKeyboardButton(
                text='Доска заявок',
                callback_data='zayavka'
            )
        ]]
    )