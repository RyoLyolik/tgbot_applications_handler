from datetime import datetime, timedelta
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constant import delta, KeyboardButtons, user_data_template, start_answer_text, end_answer_text
from exceptions import ValidationException
from filters import StatesFilter, RequestCallbackFilter
from utils import code_user, send_user_request, save_user, get_user
from validators import User, States, ValidationException, Category


dp = Dispatcher()
bot = Bot(token=os.getenv('tg_token'))


@dp.message(Command('start'))
async def cmd_start(message: Message):
    user_id = str(message.from_user.id)
    user = await get_user(user_id)
    user.state.value = States.start
    await save_user(user)
    builder = InlineKeyboardBuilder([
        [KeyboardButtons.init_set_category_L2H2],
        [KeyboardButtons.init_set_category_L2H3],
    ])
    await message.answer(start_answer_text, reply_markup=builder.as_markup(), parse_mode='HTML')


@dp.callback_query(        
    RequestCallbackFilter.filter(F.context=='make')
)
async def start_request(callback: CallbackQuery, callback_data: RequestCallbackFilter):
    user_id = str(callback.from_user.id)
    user = await get_user(user_id)
    if user.state.value == States.start:
        user.category = callback_data.category
    user.state.value = States.default
    await save_user(user)
    answer_text = '<b>Ваша заявка</b>\n' + user_data_template.format(**code_user(user))
    builder = InlineKeyboardBuilder(
        [
            [KeyboardButtons.send_reqeust],
            [KeyboardButtons.change_fullname],
            [KeyboardButtons.change_category],
            [KeyboardButtons.change_company],
            [KeyboardButtons.change_inn],
            [KeyboardButtons.change_phone_number],
        ]
    )
    await bot.edit_message_text(answer_text, chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=builder.as_markup(), parse_mode='HTML')
    await bot.answer_callback_query(callback.id)


@dp.callback_query(F.data.in_(States.values()))
async def change_userdata(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    user = await get_user(user_id)
    user.state.value = States(callback.data)
    user.state.message_id = callback.message.message_id
    await save_user(user)
    keyboard = []
    match callback.data:
        case States.change_fullname:
            answer_text = f'Введите ФИО\nТекущее ФИО: <code>{user.fullname}</code>'
        case States.change_category:
            answer_text = f'Выберите категорию\nТекущая категория: <code>{user.category}</code>'
            keyboard.append([KeyboardButtons.set_category_L2H2])
            keyboard.append([KeyboardButtons.set_category_L2H3])
        case States.change_company:
            answer_text = f'Введите название компании\nТекущая компания: <code>{user.company}</code>'
        case States.change_inn:
            answer_text = f'Введите ИНН\nТекущий ИНН: <code>{user.inn}</code>'
        case States.change_phone_number:
            answer_text = f'Введите номер телефона\nТекущий номер телефона: <code>{user.phone_number}</code>'
    keyboard.append([KeyboardButtons.done])
    builder = InlineKeyboardBuilder(keyboard)
    await bot.edit_message_text(
        answer_text,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=builder.as_markup(),
        parse_mode='HTML',
    )
    await bot.answer_callback_query(callback.id)


@dp.message(F.text, StatesFilter(States.values()))
async def changing_userdata(message: Message):
    keyboard = []
    user = await get_user(message.from_user.id)
    unsaved_user = User(**user.model_dump())
    answer_text = None
    try:
        match user.state.value:
            case States.change_fullname:
                answer_template = 'Введите ФИО\nТекущее ФИО: <code>{data_field}</code>'
                user.fullname = ' '.join(message.text.split()).title()
                answer_text = answer_template.format(data_field=unsaved_user.fullname)
                user.validate_fullname()
                answer_text = answer_template.format(data_field=user.fullname)
            case States.change_company:
                user.company = message.text
                answer_text = f'Введите название компании\nТекущая компания: <code>{user.company}</code>'
            case States.change_inn:
                answer_template = 'Введите ИНН\nТекущий ИНН: <code>{data_field}</code>'
                user.inn = message.text
                answer_text = answer_template.format(data_field=unsaved_user.inn)
                user.validate_inn()
                answer_text = answer_template.format(data_field=user.inn)
            case States.change_phone_number:
                answer_template = 'Введите номер телефона\nТекущий номер телефона: <code>{data_field}</code>'
                user.phone_number = message.text
                answer_text = answer_template.format(data_field=unsaved_user.phone_number)
                user.validate_phone_number()
                answer_text = answer_template.format(data_field=user.phone_number)
        await save_user(user)
    except ValidationException as e:
        answer_text += f'\n\n❗️Ошибка:\n<code>{message.text}</code> - не подходит\n{e}'
    keyboard.append([KeyboardButtons.done])
    builder = InlineKeyboardBuilder(keyboard)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    try:
        if answer_text:
            await bot.edit_message_text(
                answer_text,
                chat_id=message.chat.id,
                message_id=user.state.message_id,
                reply_markup=builder.as_markup(),
                parse_mode='HTML'
            )
    except TelegramBadRequest:
        pass


@dp.callback_query(
        RequestCallbackFilter.filter(F.context=='chng'),
        RequestCallbackFilter.filter(F.category.in_((Category.L2H2, Category.L2H3)))
)
async def changing_category(callback: CallbackQuery, callback_data: RequestCallbackFilter):
    user = await get_user(callback.from_user.id)
    user.category = Category(callback_data.category)
    await save_user(user)
    keyboard = [
        [KeyboardButtons.set_category_L2H2],
        [KeyboardButtons.set_category_L2H3],
        [KeyboardButtons.done],
    ]
    builder = InlineKeyboardBuilder(keyboard)
    try:
        await bot.edit_message_text(
            f'Выберите категорию\nТекущая категория: <code>{user.category}</code>',
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=builder.as_markup(),
            parse_mode='HTML',
        )
    except TelegramBadRequest:
        pass
    await bot.answer_callback_query(callback.id)


@dp.callback_query(F.data=='send_request')
async def sending_request(callback: CallbackQuery):
    user = await get_user(str(callback.from_user.id))
    keyboard = []
    empty_fields = user.get_empty_fields()
    if datetime.timestamp(datetime.now()) - user.timestamp < delta:
        left_seconds = delta - (datetime.timestamp(datetime.now()) - user.timestamp)
        answer_text = f'Вы уже отправляли заявку в последнее время, подождите {timedelta(seconds=int(left_seconds))}'
        keyboard = [[KeyboardButtons.ok]]
    elif empty_fields:
        answer_text = '❗️ Заявка заполнена не полностью\nНезаполненные поля:\n'
        answer_text += '\n'.join(map(lambda field: ' • '+field, empty_fields))
        keyboard = [[KeyboardButtons.fill_request]]
    else:
        send_user_request(user)
        user.timestamp = datetime.now().timestamp()
        await save_user(user)
        answer_text = end_answer_text
    builder = InlineKeyboardBuilder(keyboard)
    try:
        await bot.edit_message_text(
            answer_text,
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=builder.as_markup(),
            parse_mode='HTML',
        )
    except TelegramBadRequest:
        pass
