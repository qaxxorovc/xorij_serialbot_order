from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from database.base import movie_table, users_table, channels_table,Serial_table,create_admins_table
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from middlewares.subscription import CheckSubscriptionMiddleware

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await movie_table()
    await create_admins_table()
    await users_table()
    await Serial_table()
    await channels_table()
    await on_startup_notify(dispatcher)

dp.middleware.setup(CheckSubscriptionMiddleware())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
