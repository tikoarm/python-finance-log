import sys
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules', 'database'))

import settings
from SqlCode import dbmanager, db

bot = Bot(token=settings.tg_token)
dp = Dispatcher(bot)

# Обработчик команды /safe
@dp.message_handler(commands=['safe'])
async def safe(message: types.Message):
    tg_id = message.from_user.id
    safes = dbmanager.get_safes_by_owner(db, tg_id)
    
    if not safes:
        await message.reply("Нет сейфов для данного пользователя.")
        return

    keyboard = InlineKeyboardMarkup(row_width=1)
    for safe_id, safe_name in safes:
        keyboard.add(InlineKeyboardButton(text=safe_name, callback_data=f'safe_{safe_id}'))
    
    await bot.send_message(message.from_user.id, "🗄 Выберите сейф: 🗄", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('safe_'))
async def process_callback_button(callback_query: types.CallbackQuery):
    safeid = int(callback_query.data.split('_')[1])
    string = dbmanager.get_safe_name(db, safeid)
    settings.CurrentSafe[callback_query.message.chat.id] = safeid

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Информация", callback_data=f'safeaction_info'))
    keyboard.add(InlineKeyboardButton(text="Изменить название", callback_data=f'safeaction_setname'))
    keyboard.add(InlineKeyboardButton(text="Пополнить", callback_data=f'safeaction_add'))
    keyboard.add(InlineKeyboardButton(text="Снять", callback_data=f'safeaction_take'))

    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f"Вы успешно выбрали копилку <b>« {string} »</b>\nПожалуйста, выберите желаемое действие", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    await bot.answer_callback_query(callback_query.id)

# Обработчик нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('safeaction_'))
async def process_callback_button(callback_query: types.CallbackQuery):
    button_name = callback_query.data
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=None)
    await bot.answer_callback_query(callback_query.id)

    if button_name == "safeaction_info":
        string = await settings.base_utils.safe_information_str(settings.CurrentSafe[callback_query.message.chat.id])
        await bot.send_message(callback_query.from_user.id, string, parse_mode=types.ParseMode.HTML)
        return 1

    elif button_name == "safeaction_add":
        await bot.send_message(callback_query.from_user.id, "💸 Пожалуйста, введите сумму, на которую желаете <b>пополнить</b> свою копилку: 💸", parse_mode=types.ParseMode.HTML)
        settings.CurrentAction[callback_query.message.chat.id] = button_name
        return 1

    elif button_name == "safeaction_take":
        await bot.send_message(callback_query.from_user.id, "💸 Пожалуйста, введите сумму, на которую желаете <b>снять</b> со своей копилки: 💸", parse_mode=types.ParseMode.HTML)
        settings.CurrentAction[callback_query.message.chat.id] = button_name
        return 1

    elif button_name == "safeaction_setname":
        await bot.send_message(callback_query.from_user.id, "🗄 Пожалуйста, введите новое <b>название</b> своей копилки: 🗄", parse_mode=types.ParseMode.HTML)
        settings.CurrentAction[callback_query.message.chat.id] = button_name
        return 1

    else:
        await bot.send_message(callback_query.from_user.id, f"Unknown button: <b>{button_name}</b>", parse_mode=types.ParseMode.HTML)

@dp.message_handler()
async def playertext(message: types.Message):
    if message.chat.id in settings.CurrentAction and settings.CurrentAction[message.chat.id] == "safeaction_add":
        if not message.text.isdigit():
            await message.reply("Ошибка! Пожалуйста, отправьте только цифры.")
            return

        summa = int(message.text)
        settings.CurrentAction[message.chat.id] = ""
        string = await settings.base_utils.add_cash_to_safe(settings.CurrentSafe[message.chat.id], summa)
        await bot.send_message(message.from_user.id, string, parse_mode=types.ParseMode.HTML)
        return 1

    elif message.chat.id in settings.CurrentAction and settings.CurrentAction[message.chat.id] == "safeaction_take":
        if not message.text.isdigit():
            await message.reply("Ошибка! Пожалуйста, отправьте только цифры.")
            return

        summa = int(message.text)
        settings.CurrentAction[message.chat.id] = ""
        string = await settings.base_utils.take_cash_from_safe(settings.CurrentSafe[message.chat.id], summa)
        await bot.send_message(message.from_user.id, string, parse_mode=types.ParseMode.HTML)
        return 1
    
    elif message.chat.id in settings.CurrentAction and settings.CurrentAction[message.chat.id] == "safeaction_setname":
        name = message.text
        if len(name) < 3 or len (name) > 32:
            await message.reply("Пожалуйста, введите название от 3 до 32 символов!")
            return

        settings.CurrentAction[message.chat.id] = ""
        string = await settings.base_utils.set_safe_name(settings.CurrentSafe[message.chat.id], name)
        await bot.send_message(message.from_user.id, string, parse_mode=types.ParseMode.HTML)
        return 1

async def start():
    await dp.start_polling()