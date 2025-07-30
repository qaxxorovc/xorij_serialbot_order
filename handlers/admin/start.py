from aiogram import types
from loader import dp,bot
from filters.adminchecker import IsAdmin
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu
from aiogram.types import CallbackQuery
from aiogram.types import InputFile
from database.base import *
from keyboards.inline.keyrboards import *
from data.config import *
from aiogram.types import ReplyKeyboardRemove
from states.state import *


@dp.message_handler(IsAdmin(),commands=['start','help'],state="*")
async def admin_message(message: types.Message, state: FSMContext):
    await message.reply(
        "👮‍♂️ Siz adminsiz! O'z huquqlaringizdan foydalaning! 🎛️", 
        reply_markup=adminmenu
    )
    await state.finish()


    get_fake_links = await get_all_links()

    if get_fake_links:
        print(get_fake_links)


@dp.message_handler(IsAdmin(),text="🛠️ Bakor qilish",state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(
        "👮‍♂️ Bekor qilindi", 
        reply_markup=ReplyKeyboardRemove()
    )
    await message.reply(
        "👮‍♂️ Siz adminsiz! O'z huquqlaringizdan foydalaning! 🎛️", 
        reply_markup=adminmenu
    )
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data == "getdata")
async def handle_upload_data(callback_query: CallbackQuery):
    text = await getinfo()
    await callback_query.message.answer(text)

@dp.callback_query_handler(lambda callback_query: callback_query.data == "upload_data")
async def handle_upload_data(callback_query: CallbackQuery):
    # Ma'lumotlar bazasining fayl yo'lini aniqlash
    db_file_path = 'database.db'  # Fayl yo'lini o'zgartirishingiz mumkin

    if os.path.exists(db_file_path):
        # Faylni ochish
        with open(db_file_path, 'rb') as db_file:
            # Foydalanuvchiga yuborish
            await bot.send_document(callback_query.message.chat.id, db_file)
            await callback_query.answer("Ma'lumotlar bazasi yuborildi.", show_alert=True)
    else:
        await callback_query.answer("Ma'lumotlar bazasi topilmadi.", show_alert=True)
