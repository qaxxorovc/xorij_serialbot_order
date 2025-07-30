from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu, cancel, bot_channel, trailer_keyboard
from states.state import *
from filters.adminchecker import IsAdmin
from data.config import *
from database.base import *
from aiogram.types import ReplyKeyboardRemove

@dp.callback_query_handler(IsAdmin(), text="add_movie")
async def add_movie(callback_query: CallbackQuery):
    await callback_query.message.answer("🎬 Kino nomini kiriting:", reply_markup=cancel)
    await addmoviestate.VideoName.set()  # Video nomi so'raladi

@dp.message_handler(state=addmoviestate.VideoName)
async def process_movie_name(message: types.Message, state: FSMContext):
    movie_name = message.text.strip()
    await state.update_data(MovieName=movie_name)
    await message.answer("📔 Kino kodini kiriting (masalan: 1 2 3...):")
    await addmoviestate.FilmCode.set()

@dp.message_handler(state=addmoviestate.FilmCode)
async def process_film_code(message: types.Message, state: FSMContext):
    code = message.text.strip()  # Admin tomonidan kiritilgan kod
    await state.update_data(MovieCode=code)
    await message.answer("📹 Kinoni jo'nating:")
    await addmoviestate.Video.set()

@dp.message_handler(state=addmoviestate.Video, content_types=ContentType.VIDEO)
async def process_video(message: types.Message, state: FSMContext):
    video = message.video
    file_id = video.file_id
    await state.update_data(Video=file_id)
    await message.answer("✅ Video qabul qilindi. Tavsifni kiriting:")
    await message.answer(f"""
📹 Sifati: 
📆 Yili: 
🎞 Janri: 
🇺🇸 Davlati: 
🇺🇿 Tili: 
                             
🤖Bizning bot: @{BOTUSERNAME}
""")
    await addmoviestate.VideoCaption.set()

@dp.message_handler(state=addmoviestate.VideoCaption)
async def process_caption(message: types.Message, state: FSMContext):
    movie_name = (await state.get_data()).get('MovieName')
    movie_code = (await state.get_data()).get('MovieCode')
    caption_text = message.text.strip()

    caption = f"""
🎥 Nomi: {movie_name}

{caption_text}

📔 Code: `{movie_code}`
"""
    await state.update_data(VideoCaption=caption)

    video = (await state.get_data()).get('Video')
    caption = (await state.get_data()).get('VideoCaption')
    newcaption = f"{caption}\n0Hoziroq tomosha qiling👀"
    
    await addmoviebot(str(video), str(caption), str(movie_code))
    await message.answer("🎥 Trailer mavjudmi?", reply_markup=trailer_keyboard)
    await addmoviestate.Trailer.set()

@dp.callback_query_handler(state=addmoviestate.Trailer, text="add_trailer")
async def add_trailer(callback_query: CallbackQuery):
    await callback_query.message.answer("📹 Trailerni jo'nating:", reply_markup=cancel)
    await addmoviestate.TrailerVideo.set()

@dp.message_handler(state=addmoviestate.TrailerVideo, content_types=ContentType.VIDEO)
async def process_trailer(message: types.Message, state: FSMContext):
    trailer = message.video.file_id
    video = (await state.get_data()).get('Video')
    caption = (await state.get_data()).get('VideoCaption')
    movie_code = (await state.get_data()).get('MovieCode')
    trailer_caption = f"{caption}\n🎥 Trailer:"
    await state.finish()
    try:
        await bot.send_video(chat_id=FILMSDATAID, video=trailer, caption=trailer_caption, parse_mode=types.ParseMode.MARKDOWN, reply_markup=bot_channel)
        await message.answer("✅ Kino va trailer muvaffaqiyatli qo'shildi!\n\nKino: {movie_code}", reply_markup=adminmenu)
    except:
        await message.answer(f"❌ Ushbu kino kalaga yuborilmadi. Ammo DB qo'shildi\n\nKino: {movie_code}", reply_markup=adminmenu)
@dp.callback_query_handler(state=addmoviestate.Trailer, text="no_trailer")
async def no_trailer(callback_query: CallbackQuery, state: FSMContext):
    movie_code = (await state.get_data()).get('MovieCode')
    video = (await state.get_data()).get('Video')
    caption = (await state.get_data()).get('VideoCaption')
    await state.finish()
    try:
        await bot.send_message(chat_id=FILMSDATAID, text=caption, reply_markup=bot_channel)
        await callback_query.message.answer(f"✅ Kino va trailer muvaffaqiyatli qo'shildi!\n\nKino: {movie_code}", reply_markup=adminmenu)
    except:
        await callback_query.message.answer(f"❌ Ushbu kino kalaga yuborilmadi. Ammo DB qo'shildi\n\nKino: {movie_code}", reply_markup=adminmenu)