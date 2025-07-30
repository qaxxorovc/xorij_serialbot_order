from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import *


FILMSDATABUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Do'stlarga ulashish 📲",url=f"https://t.me/share/url?url=Men%20bu%20botni%20tavsiya%20qilaman!%20🤖✨%20@{BOTUSERNAME}"),
        ],
    ]
)

adminmenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📢 Foydalanuvchilarga habar jo'natish", callback_data="send_message"),
        ],
        [
            InlineKeyboardButton(text="➕ Majburiy obuna kanalini qo'shish", callback_data="add_subscription"),
            InlineKeyboardButton(text="❌ Majburiy obuna kanalini O'chirish", callback_data="remove_subscription"),
        ],
        [
            InlineKeyboardButton(text="➕ Soxta link qo'shish", callback_data="add_fake_link"),
            InlineKeyboardButton(text="❌ Soxta link O'chirish", callback_data="remove_fake_link"),
        ],
        [
            InlineKeyboardButton(text="🎬 Serial qo'shish", callback_data="add_serial"),
            InlineKeyboardButton(text="🗑️ Serial o'chirish", callback_data="remove_serial"),
        ],
        [
            InlineKeyboardButton(text="🎬 Film qo'shish", callback_data="add_movie"),
            InlineKeyboardButton(text="🗑️ Film o'chirish", callback_data="remove_movie"),
        ],
        [
            InlineKeyboardButton(text="👤 Admin qo'shish", callback_data='addadmin'),
        ],
        [
            InlineKeyboardButton(text="👥 Adminlar", callback_data='admins'),
        ],
        [
            InlineKeyboardButton(text="📄 Malumotlar raqam ko'rinishida yuklash", callback_data="getdata"),
        ],
        [
            InlineKeyboardButton(text="📄 Malumotlar filesini yuklash", callback_data="upload_data"),
        ],
    ]
)

cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛠️ Bakor qilish", callback_data="backup"),
        ],
    ]
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🤖 Bizning Bot", url=f"https://t.me/{BOTUSERNAME}"),
        ],
        [
            InlineKeyboardButton(text="📢 Kanalimizga Qo‘shiling", url=f"https://t.me/{FILMSDATAURL}")
        ]
    ]
)

trailer_keyboard = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("🎥 Ha, trailer bor", callback_data="add_trailer"),
    InlineKeyboardButton("🚫 Yo'q", callback_data="no_trailer")
)