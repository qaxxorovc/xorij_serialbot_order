from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keys = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1️⃣ Raqami orqali"),
        ],
        [
            KeyboardButton(text="2️⃣ Qismi orqali"),
        ],
        [
            KeyboardButton(text="🛠️ Bakor qilish"),
        ]
    ],
    resize_keyboard=True 
)
