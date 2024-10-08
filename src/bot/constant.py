from aiogram.types import InlineKeyboardButton
from validators import States, Category


user_data_template = \
''' • ФИО: {fullname}
 • Категория: {category}
 • Компания: {company}
 • ИНН: {inn}
 • Номер телефона для связи: {phone_number}'''

delta = 3600 # кулдаун отправки заявок в секундах

class KeyboardButtons:
    create_reqeust = InlineKeyboardButton(text='Оставить заявку', callback_data='create_request')
    send_reqeust = InlineKeyboardButton(text='✉️ Отправить заявку', callback_data='send_request')
    change_fullname = InlineKeyboardButton(text='Изменить ФИО', callback_data=States.change_fullname)
    change_category = InlineKeyboardButton(text='Изменить категорию', callback_data=States.change_category)
    change_company = InlineKeyboardButton(text='Изменить компанию', callback_data=States.change_company)
    change_inn = InlineKeyboardButton(text='Изменить ИНН', callback_data=States.change_inn)
    change_phone_number = InlineKeyboardButton(text='Изменить номер телефона', callback_data=States.change_phone_number)
    set_category_HT = InlineKeyboardButton(text='1. Категория HT', callback_data=Category.HT)
    set_category_MT = InlineKeyboardButton(text='2. Категория MT', callback_data=Category.MT)
    done = InlineKeyboardButton(text='✅ Готово', callback_data='create_request')
    ok = InlineKeyboardButton(text='Ок', callback_data='create_request')
    fill_request = InlineKeyboardButton(text='Заполнить заявку', callback_data='create_request')
