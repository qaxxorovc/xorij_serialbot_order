from aiogram import types
from loader import dp,bot
from aiogram.dispatcher import FSMContext
from filters.adminchecker import IsAdmin
from keyboards.inline.keyrboards import adminmenu
from aiogram.types import CallbackQuery
from database.base import *
from keyboards.inline.keyrboards import *
from data.config import *
from aiogram.types import ReplyKeyboardRemove
from states.state import *



@dp.callback_query_handler(text="remove_subscription")
async def remove_channel(callback_query: CallbackQuery):
    conn, cur = await connect_db()
    cur.execute("SELECT ChannelName, Channelusername, Channelid FROM Channels")
    all_channels = cur.fetchall()
    conn.close()

    if all_channels:
        channel_info = "📋 Barcha majburiy kanallar:\n"
        for channel in all_channels:
            channel_name, channel_username, channel_id = channel
            channel_info += f"📝 Kanal nomi: {channel_name}\n" \
                            f"🔗 Kanal username: @{channel_username}\n" \
                            f"🆔 Kanal ID: {channel_id}\n\n"
        await callback_query.message.answer(channel_info)
    else:
        await callback_query.message.answer("🚫 Hozirda kanallar mavjud emas.")
    await callback_query.message.answer("🛑 O'chirmoqchi bo'lgan kanalni idsini kiriting:", reply_markup=cancel)
    await detelechannel.channelid.set()

@dp.message_handler(state=detelechannel.channelid)
async def process_remove_channel(message: types.Message, state: FSMContext):       
    if message.text == "🛠️ Bakor qilish":
        await message.answer("❌ Bekor qilindi", reply_markup=adminmenu)
        await state.finish()
    else:       
        channelid = message.text.strip()
        await deletechannelcheck(channelid)
        await message.answer("✅ Kanal majburiy obuna qismidan o'chirildi!", reply_markup=adminmenu)
        await state.finish()
