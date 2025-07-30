from aiogram.dispatcher.filters.state import State, StatesGroup

class FakeLinkState(StatesGroup):
    waiting_for_title = State()
    waiting_for_link = State()


from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from loader import dp
from database.base import add_link, remove_link_by_id, get_all_links
from filters.adminchecker import IsAdmin
from keyboards.inline.keyrboards import cancel, adminmenu

# ➕ Soxta link qo‘shish
@dp.callback_query_handler(IsAdmin(), text="add_fake_link")
async def handle_add_fake_link(call: types.CallbackQuery):
    await call.message.answer("📝 Soxta link uchun nom kiriting:", reply_markup=cancel)
    await FakeLinkState.waiting_for_title.set()
    await call.answer()

@dp.message_handler(state=FakeLinkState.waiting_for_title)
async def receive_link_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer("🔗 Endi linkni yuboring (faqat `https://` bilan boshlanishi kerak):", reply_markup=cancel)
    await FakeLinkState.waiting_for_link.set()

@dp.message_handler(state=FakeLinkState.waiting_for_link)
async def receive_link_url(message: types.Message, state: FSMContext):
    link = message.text.strip()
    if not link.startswith("https://"):
        await message.answer("❌ Link noto‘g‘ri formatda. U `https://` bilan boshlanishi kerak. Qaytadan kiriting:", reply_markup=cancel)
        return

    data = await state.get_data()
    title = data['title']
    await add_link(title, link)
    await message.answer("✅ Soxta link muvaffaqiyatli qo‘shildi.", reply_markup=adminmenu)
    await state.finish()

@dp.callback_query_handler(text="remove_fake_link")
async def handle_remove_fake_link(call: types.CallbackQuery):
    links = await get_all_links()
    if not links:
        await call.message.answer("⚠️ Hech qanday soxta link mavjud emas.", reply_markup=adminmenu)
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for link_id, title, link in links:
        markup.add(
            InlineKeyboardButton(
                text=f"{title} ❌",
                callback_data=f"delete_fake:{link_id}"
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=f"❌ Bekor qilish",
            callback_data=f"backup"
        )
    )

    await call.message.answer("🗑 O‘chirmoqchi bo‘lgan linkni tanlang:", reply_markup=markup)
    await call.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("delete_fake:"))
async def confirm_delete_link(call: types.CallbackQuery):
    link_id = int(call.data.split(":")[1])
    await remove_link_by_id(link_id)
    await call.message.edit_text("✅ Link o‘chirildi.", reply_markup=adminmenu)
    await call.answer()
