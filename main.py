import asyncio
import logging

from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


from config import BOT_TOKEN
from handlers import start, create_order, order_message, zayavka


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(*[start.router, create_order.router, order_message.router, zayavka.router])
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(ChatActionMiddleware())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())