from aiogram import types
from loader import dp,bot
from filters.adminchecker import IsAdmin
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu
from aiogram.types import CallbackQuery
from database.base import *
from keyboards.inline.keyrboards import *
from data.config import *
from aiogram.types import ReplyKeyboardRemove
from states.state import *



@dp.callback_query_handler(IsAdmin(),text="send_message")
async def send_message(callback_query: CallbackQuery):
    await callback_query.message.answer("📢 Foydalanuvchilarga tashlanishi uchun reklamani [rasm,video] jo'nating\n\n❗ Tavsif jo'natmang!", reply_markup=cancel)
    await reklama.videoandcaption.set()

@dp.message_handler(state=reklama.videoandcaption, content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message, state: FSMContext):
    media = message.photo[-1].file_id
    await state.update_data(media_id=media)
    await message.answer("📜 Endi tavsifni yuboring.")
    await reklama.description.set()

@dp.message_handler(state=reklama.videoandcaption, content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message, state: FSMContext):
    media = message.video.file_id
    await state.update_data(media_id=media)
    await message.answer("📜 Endi tavsifni yuboring.")
    await reklama.description.set()

@dp.message_handler(state=reklama.videoandcaption, content_types=types.ContentType.AUDIO)
async def handle_audio(message: types.Message, state: FSMContext):
    media = message.audio.file_id
    await state.update_data(media_id=media)
    await message.answer("📜 Endi tavsifni yuboring.")
    await reklama.description.set()

@dp.message_handler(state=reklama.videoandcaption, content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message, state: FSMContext):
    media = message.document.file_id
    await state.update_data(media_id=media)
    await message.answer("📜 Endi tavsifni yuboring.")
    await reklama.description.set()

@dp.message_handler(state=reklama.videoandcaption, content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message, state: FSMContext):
    await message.answer("⚠️ Iltimos, faqat rasm, video, audio yoki hujjat yuboring.")


@dp.message_handler(state=reklama.description)
async def handle_caption(message: types.Message, state: FSMContext):
    caption = message.text
    user_data = await state.get_data()
    media_id = user_data.get("media_id")
    
    if media_id:
        user = await useridlist()
        for user_id in user:
            try:
                try:
                    await bot.send_photo(chat_id=user_id, photo=media_id, caption=caption)
                except:
                    await bot.send_video(chat_id=user_id, video=media_id, caption=caption)
            except:
                pass
        await message.answer("📤 Reklama foydalanuvchilarga yuborildi!", reply_markup=adminmenu)
        await state.finish()
