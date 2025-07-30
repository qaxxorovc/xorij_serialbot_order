from aiogram import types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from loader import dp,bot
from database.base import *
from aiogram.types import CallbackQuery
from aiogram.contrib.middlewares.fsm import FSMContext
from states.state import *
from data.config import *
from filters.adminchecker import IsAdmin
import os
from keyboards.inline.keyrboards import cancel

async def generate_admin_buttons():
    admin_ids = await get_admin_ids()
    keyboard = InlineKeyboardMarkup()

    for admin_id in admin_ids:
        admin_id = int(admin_id[0])
        print(admin_id)
        button = InlineKeyboardButton(
            text=f"👤 Admin: {admin_id}",
            callback_data=f"removeadmin:{admin_id}"
        )
        keyboard.add(button)
    back = InlineKeyboardButton("❌ Bekor qilish", callback_data="backup")
    keyboard.add(back)

    return keyboard


@dp.callback_query_handler(IsAdmin(),lambda c: c.data == 'addadmin')
async def add_admin_callback(callback_query: CallbackQuery):
    await callback_query.message.answer(
            "🆔 Qo'shmoqchi bo'lgan adminning ID sini kiriting:", reply_markup=cancel
        )
    await AdminAddState.admin_id.set()
    
@dp.message_handler(state=AdminAddState.admin_id)
async def process_add_admin(message: types.Message, state: FSMContext):
    """
    Admin IDni qabul qilish va qo'shish funksiyasi.
    """
    admin_id = message.text
    if len(admin_id) <= 4:
        await message.answer("Admin IDni to'g'ri kiriting:",reply_markup=cancel) 
    else:
        result = await add_admin(admin_id)
        if result:
            await message.answer(f"✅ Admin {admin_id} muvaffaqiyatli qo'shildi!\n\n\n/start bosing va botni qayta yuklang")
        else:
            await message.answer(f"⚠️ Admin {admin_id} allaqachon ro'yxatda mavjud yoki xato yuz berdi.\n\n\n/start bosing va botni qayta yuklang")
        await state.finish()


@dp.callback_query_handler(IsAdmin(),lambda c: c.data == 'admins')
async def remove_admin_callback(callback_query: CallbackQuery):
    keyrboard = await generate_admin_buttons()
    await callback_query.message.answer("🛑 O'chirmoqchi bo'lgan adminning ID sini bosing:", reply_markup=keyrboard)

@dp.callback_query_handler(lambda c: c.data.startswith("removeadmin:"))        
async def handle_remove_admin(callback_query: CallbackQuery):
    admin_id = int(callback_query.data.split(":")[1]) 
    result = await remove_admin(admin_id) 
    if not result:
        await callback_query.answer(f"Admin {admin_id} o'chirildi!\n\n\n/start bosing va botni qayta yuklang")
        await callback_query.message.edit_text(f"Admin {admin_id} o'chirildi!\n\n\n/start bosing va botni qayta yuklang")
    else:
        await callback_query.answer(f"Admin {admin_id} topilmadi yoki o'chirib bo'lmadi!\n\n\n/start bosing va botni qayta yuklang", show_alert=True)    
