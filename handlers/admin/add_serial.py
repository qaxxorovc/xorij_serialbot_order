from aiogram import types
from aiogram.types import CallbackQuery, ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu, cancel, bot_channel, trailer_keyboard
from states.state import addserialstate
from filters.adminchecker import IsAdmin
from data.config import FILMSDATAID,BOTUSERNAME
from database.base import add_serial_to_db, count_unique_serials

@dp.callback_query_handler(IsAdmin(), text="add_serial")
async def choose_serial_type(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("🆕 Yangi serial", callback_data="new_serial"),
        InlineKeyboardButton("♻️ Mavjud serial", callback_data="existing_serial"),
        InlineKeyboardButton(text="🛠️ Bakor qilish", callback_data="backup")
    )
    await callback_query.message.answer("🆕 Yangi serial ochasizmi yoki mavjudiga qism qo‘shasizmi?", reply_markup=keyboard)
    await addserialstate.ChooseOption.set()

@dp.callback_query_handler(state=addserialstate.ChooseOption, text="new_serial")
async def add_new_serial(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("📹 Serialni videosini jo'nating:", reply_markup=cancel)
    await addserialstate.Video.set()

@dp.callback_query_handler(state=addserialstate.ChooseOption, text="existing_serial")
async def add_existing_serial(callback_query: CallbackQuery):
    await callback_query.message.answer("🔢 Serial raqamini kiriting (Masalan: 1, 2, 3...)",reply_markup=cancel)
    await addserialstate.ExistingSerial.set()

@dp.message_handler(state=addserialstate.ExistingSerial)
async def process_existing_serial(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(SerialNumber=int(message.text))
        await message.answer("📹 Serial videosini jo‘nating:", reply_markup=cancel)
        await addserialstate.Video.set()
    else:
        await message.answer("⚠️ Iltimos, faqat raqam kiriting.")

@dp.message_handler(state=addserialstate.Video, content_types=ContentType.VIDEO)
async def process_video(message: types.Message, state: FSMContext):
    data = await state.get_data()
    serial_number = data.get("SerialNumber") or (await count_unique_serials() + 1)
    await state.update_data(Video=message.video.file_id, SerialNumber=serial_number)
    await message.answer("🔢 Serial qism raqamini kiriting (Masalan: 1, 2, 3...)",reply_markup=cancel)
    await addserialstate.SerialPart.set()

@dp.message_handler(state=addserialstate.SerialPart)
async def process_serial_part(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        serial_part = int(message.text)
        data = await state.get_data()
        code = f"{data['SerialNumber']}-{serial_part}"
        await state.update_data(SerialPart=serial_part, Code=code)
        await message.answer("✅ Serial qismi qabul qilindi. Tavsifni kiriting:")
        await message.answer(f"""
🎥 Nomi:
📹 Sifati:
📆 Yili:
🎞 Janri:
🇺🇸 Davlati:
🇺🇿 Tili:

🤖Bizning bot: @{BOTUSERNAME}
""")
        await addserialstate.VideoCaption.set()
    else:
        await message.answer("⚠️ Iltimos, faqat raqam kiriting.")

@dp.message_handler(state=addserialstate.VideoCaption)
async def process_caption(message: types.Message, state: FSMContext):
    data = await state.get_data()
    caption = f"""
{message.text}

📔 Code: `{data['Code']}`
"""
    await state.update_data(VideoCaption=caption)
    await message.answer("🎥 Trailer mavjudmi?", reply_markup=trailer_keyboard)
    await add_serial_to_db(data['Video'], caption, data['SerialNumber'], data['SerialPart'])
    await addserialstate.Trailer.set()

@dp.callback_query_handler(state=addserialstate.Trailer, text="add_trailer")
async def add_trailer(callback_query: CallbackQuery):
    await callback_query.message.answer("📹 Trailerni jo'nating:", reply_markup=cancel)
    await addserialstate.TrailerVideo.set()

@dp.message_handler(state=addserialstate.TrailerVideo, content_types=ContentType.VIDEO)
async def process_trailer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    trailer_caption = f"{data['VideoCaption']}\n🎥 Trailer:"
    await ask_to_add_another_part(message, state)
    try:
        await bot.send_video(FILMSDATAID, message.video.file_id, caption=trailer_caption, parse_mode=types.ParseMode.MARKDOWN, reply_markup=bot_channel)
        await message.answer("Triller kanalga jo'natildi,Serial botga qo'shildi")
    except:
        await message.answer("Trailerni jo'natishda xatolik yuz berdi, Ammo serial botga qo'shildi")
@dp.callback_query_handler(state=addserialstate.Trailer, text="no_trailer")
async def no_trailer(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await ask_to_add_another_part(callback_query.message, state)
    await bot.send_message(FILMSDATAID, data['VideoCaption'], parse_mode=types.ParseMode.MARKDOWN, reply_markup=bot_channel)

async def ask_to_add_another_part(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("➕ Yana qo‘shish", callback_data="add_more"),
        InlineKeyboardButton("✅ Tugatish", callback_data="finish")
    )
    await message.answer("❓ Yana qism qo'shasizmi yoki tugatasizmi?", reply_markup=keyboard)
    await addserialstate.Confirm.set()

@dp.callback_query_handler(IsAdmin(), text="add_more", state=addserialstate.Confirm)
async def add_more(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("📹 Keyingi serial qismini jo'nating:")
    await addserialstate.Video.set()

@dp.callback_query_handler(IsAdmin(), text="finish", state=addserialstate.Confirm)
async def finish_adding(callback_query: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.answer("✅ Seriallar muvaffaqiyatli qo'shildi!", reply_markup=adminmenu)