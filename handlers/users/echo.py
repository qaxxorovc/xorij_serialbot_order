from aiogram import types
from aiogram.types import ReplyKeyboardRemove 
from loader import dp, bot
from keyboards.inline.keyrboards import FILMSDATABUTTON
from data.config import *
from database.base import *

@dp.message_handler()
async def start_handler(message: types.Message):
    text = message.text

    if "-" in text:
        try:
            serialnumber, serialpart = text.split("-")
            serialid, serialcaption = await get_serial(serialnumber, serialpart)

            if serialid:
                await bot.send_video(video=serialid, caption=serialcaption, chat_id=message.chat.id, reply_markup=FILMSDATABUTTON)
            else:
                await message.answer(f"🎬 Serial topilmadi! 😞📺", reply_markup=FILMSDATABUTTON)
        except Exception as e:
            await message.answer(f"🎬 Kino topilmadi! 😞📺", reply_markup=FILMSDATABUTTON)
    else:
        try:
            code = message.text
            movie = await findmovie(code)

            if movie:
                video_id_or_url = movie[0]
                caption = movie[1]
                await bot.send_video(video=video_id_or_url, caption=caption, chat_id=message.chat.id, reply_markup=FILMSDATABUTTON)
            else:
                await message.answer(f"🎬 Kino topilmadi! 😞📺", reply_markup=FILMSDATABUTTON)
        except Exception as e:
            await message.answer(f"🎬 Kino topilmadi! 😞📺", reply_markup=FILMSDATABUTTON)