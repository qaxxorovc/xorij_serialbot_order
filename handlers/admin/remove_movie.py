from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu, cancel
from states.state import *
from filters.adminchecker import IsAdmin
from keyboards.default.keys import keys
from data.config import *
from database.base import *
from aiogram.types import ReplyKeyboardRemove





@dp.callback_query_handler(text="remove_serial")
async def remove_serial(callback_query: CallbackQuery):
    await callback_query.message.answer("🎬 Serialni qanday o'chirasiz?\n1️⃣ Raqami orqali\n2️⃣ Qismi orqali", reply_markup=keys)
    await deteleserial.NumberOrPart.set()


@dp.message_handler(state=deteleserial.NumberOrPart)
async def choose_serial_type(message: types.Message, state: FSMContext):
    choice = message.text.strip()
    
    if choice == "1️⃣ Raqami orqali":
        await message.answer("🔢 Serialning raqamini kiriting:",reply_markup=cancel)
        await deteleserial.serialNumber.set()
    
    elif choice == "2️⃣ Qismi orqali":
        await message.answer("🔢 Serial raqamini kiriting (masalan: 2-4 formatida):",reply_markup=cancel)
        await deteleserial.serialPart.set()
    
    else:
        await message.answer("⚠️ Iltimos, to'g'ri variantni tanlang.\n1️⃣ Raqami orqali yoki 2️⃣ Qismi orqali.",reply_markup=adminmenu)


@dp.message_handler(state=deteleserial.serialNumber)
async def process_serial_number(message: types.Message, state: FSMContext):
    serial_number = message.text.strip()
    
    conn, cur = await connect_db()
    cur.execute("DELETE FROM Serials WHERE SerialNumber = ?", (serial_number,))
    conn.commit()
    conn.close()

    await message.answer(f"✅ {serial_number} raqamli serial muvaffaqiyatli o'chirildi!",reply_markup=adminmenu)
    await state.finish()


@dp.message_handler(state=deteleserial.serialPart)
async def process_serial_part(message: types.Message, state: FSMContext):
    serial_part = message.text.strip()
    
    try:
        serial_number, serial_part = map(int, serial_part.split('-'))
    except ValueError:
        await message.answer("⚠️ Iltimos, formatni to'g'ri kiriting (masalan: 2-4).",reply_markup=cancel)
        return

    conn, cur = await connect_db()
    cur.execute("DELETE FROM Serials WHERE SerialNumber = ? AND SerialPart = ?", (serial_number, serial_part))
    conn.commit()
    conn.close()

    await message.answer(f"✅ {serial_number}-{serial_part} qism serial muvaffaqiyatli o'chirildi!",reply_markup=adminmenu)
    await state.finish()




@dp.callback_query_handler(text="remove_movie")
async def remove_movie(callback_query: CallbackQuery):
    await callback_query.message.answer("🎬 Kino kodini jo'nating:", reply_markup=cancel)
    await detelemovie.moviecode.set()

@dp.message_handler(state=detelemovie.moviecode)
async def process_remove_movie(message: types.Message, state: FSMContext):         
    code = message.text
    await deletemoviebot(code)
    await message.answer("✅ Kino botdan o'chirildi!", reply_markup=adminmenu)
    await state.finish()
