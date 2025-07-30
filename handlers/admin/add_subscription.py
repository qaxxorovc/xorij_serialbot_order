from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from filters.adminchecker import IsAdmin
from keyboards.inline.keyrboards import adminmenu, cancel
from aiogram.types import CallbackQuery
from database.base import *
from states.state import *

# Callback handler for "add_subscription"
@dp.callback_query_handler(IsAdmin(), text="add_subscription")
async def add_channel(callback_query: CallbackQuery):
    conn, cur = await connect_db()
    cur.execute("SELECT ChannelName, Channelusername, Channelid FROM Channels")
    all_channels = cur.fetchall()
    conn.close()
    if all_channels:
        channel_info = "📋 Barcha majburiy kanallar:\n"
        for channel in all_channels:
            if len(channel) == 3:
                try:
                    channel_name, channel_username, channel_id = channel
                    channel_info += f"📝 Kanal nomi: {channel_name}\n" \
                                    f"🔗 Kanal username: @{channel_username}\n" \
                                    f"🆔 Kanal ID: {channel_id}\n\n"
                except ValueError:
                    channel_info += "🚫 Kanal ma'lumotlarida xatolik.\n"
            else:
                channel_info += "🚫 Kanal ma'lumotlarida xato: noto'g'ri tuzilma.\n"
        await callback_query.message.answer(channel_info)
    else:
        await callback_query.message.answer("🚫 Hozirda kanallar mavjud emas.")
    await callback_query.message.answer(
        "📑 Obuna bo'lish majburiy bo'lgan kanalni qo'shish uchun nimalar kerakligini o'qib chiqing:\n\n"
        "📌 Kanal nomi\n📌 Kanalning usernamesi\n📌 Kanalning idsi\n\n"
        "⚠️ Bot majburiy obuna qo'shilgan telegram kanalda admin bo'lishi kerak."
    )
    await callback_query.message.answer(
        "Agar barchasi tayyor bo'lsa kanalni post orqali yuboring:",
        reply_markup=cancel
    )
    await addchannel.name.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=addchannel.name)
async def process_channel_post(message: types.Message, state: FSMContext):
    channel_name = message.forward_from_chat.title
    channel_username = message.forward_from_chat.username
    channel_id = message.forward_from_chat.id
    
    try:
        administrators = await bot.get_chat_administrators(channel_id)
        bot_is_admin = any(admin.user.id == bot.id for admin in administrators)
        
        if bot_is_admin:
            await addchannelcheck(channel_name, channel_username, channel_id)
            await message.answer(
                f"✅ Kanal nomi: {channel_name},\nUsername: {channel_username},\nID: {channel_id} olindi.\n📲 Kanal majburiy obunaga qo'shildi!",
                reply_markup=adminmenu
            )
        else:
            await message.answer(
                "⚠️ Bot kanalda admin emas. Iltimos, botni kanalga admin qilib qo'ying.",
            reply_markup=cancel
            )
    
    except Exception as e:
        await message.answer(
            "⚠️ Bot kanalda admin emas. Iltimos, botni kanalga admin qilib qo'ying.",
            reply_markup=cancel
        )
    
    await state.finish()
