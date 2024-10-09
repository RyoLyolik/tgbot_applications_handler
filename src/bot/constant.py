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
    from filters import RequestCallbackFilter
    send_reqeust = InlineKeyboardButton(text='✉️ Отправить заявку', callback_data='send_request')
    change_fullname = InlineKeyboardButton(text='Изменить ФИО', callback_data=States.change_fullname)
    change_category = InlineKeyboardButton(text='Изменить категорию', callback_data=States.change_category)
    change_company = InlineKeyboardButton(text='Изменить компанию', callback_data=States.change_company)
    change_inn = InlineKeyboardButton(text='Изменить ИНН', callback_data=States.change_inn)
    change_phone_number = InlineKeyboardButton(text='Изменить номер телефона', callback_data=States.change_phone_number)
    set_category_L2H2 = InlineKeyboardButton(text='1. Normax One L2H2 (высота – 2 375 мм)', callback_data=RequestCallbackFilter(context='chng', category=Category.L2H2).pack())
    set_category_L2H3 = InlineKeyboardButton(text='2. Normax One L2H3 (высота – 2 590 мм)', callback_data=RequestCallbackFilter(context='chng', category=Category.L2H3).pack())
    init_set_category_L2H2 = InlineKeyboardButton(text='1. Normax One L2H2 (высота – 2 375 мм)', callback_data=RequestCallbackFilter(context='make', category=Category.L2H2).pack())
    init_set_category_L2H3 = InlineKeyboardButton(text='2. Normax One L2H3 (высота – 2 590 мм)', callback_data=RequestCallbackFilter(context='make', category=Category.L2H3).pack())
    done = InlineKeyboardButton(text='✅ Готово', callback_data=RequestCallbackFilter(context='make').pack())
    ok = InlineKeyboardButton(text='Ок', callback_data=RequestCallbackFilter(context='make').pack())
    fill_request = InlineKeyboardButton(text='Заполнить заявку', callback_data=RequestCallbackFilter(context='make').pack())


start_answer_text = '''Вас приветствует компания NORMAX.
Мы производим цельнометаллический коммерческий транспорт.
Наши автомобили оснащены 2-х литровым мотором на 143 л.с. (Renault) на переднем приводе! 
Удобный в использовании и комфортный автомобиль с легкостью вмещает в себя 4 Европалета.
Led фары и обогрев боковых зеркал способствует удобству в холодное время года.
Больше информации вы можете получить на нашем сайте <a href="https://normax-auto.ru/">NORMAX</a>
Для оформления заявки выберете подходящую Вам конфигурацию автомобиля.
<b>1. Normax One L2H2 (высота – 2 375 мм)</b>
<b>2. Normax One L2H3 (высота – 2 590 мм)</b>'''

end_answer_text = '''✅ Заявка успешно отправлена
Благодарим Вас за проявленный интерес к нашей марке NORMAX.
Наши специалисты свяжутся с Вами в ближайшее время!'''
