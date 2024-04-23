from aiogram import types

b1 = types.KeyboardButton(text='НХЛ')
b2 = types.KeyboardButton(text='КХЛ')

kb_user = types.ReplyKeyboardMarkup(resize_keyboard=True)

kb_user.row(b1, b2)