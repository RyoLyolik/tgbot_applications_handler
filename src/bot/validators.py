from enum import Enum
from pydantic import BaseModel, PositiveInt

from exceptions import ValidationException


class States(str, Enum):
    default = ''
    start = 'start'
    change_fullname = 'change_fullname'
    change_category = 'change_category'
    change_company = 'change_company'
    change_inn = 'change_inn'
    change_phone_number = 'change_phone_number'

    @classmethod
    def values(cls) -> list:
        return list(map(lambda el: cls._member_map_[el]._value_, cls._member_names_))


class UserState(BaseModel):
    value: States = States.default
    message_id: int = 0


class Category(str, Enum):
    default = '-'
    L2H2 = 'Normax One L2H2 (высота – 2 375 мм)'
    L2H3 = 'Normax One L2H3 (высота – 2 590 мм)'

    @classmethod
    def values(cls) -> list:
        return list(map(lambda el: cls._member_map_[el]._value_, cls._member_names_))


class User(BaseModel):
    id: str | int = None
    fullname: str = '-'
    category: Category = Category.default
    company: str = '-'
    inn: str = '-'
    phone_number: str = '-'
    timestamp: float = 0
    state: UserState = UserState()

    def get_empty_fields(self) -> list:
        empty_fields = []
        if self.fullname == '-':
            empty_fields.append('ФИО')
        if self.category == Category.default:
            empty_fields.append('Категория')
        if self.company == '-':
            empty_fields.append('Компания')
        if self.inn == '-':
            empty_fields.append('ИНН')
        if self.phone_number == '-':
            empty_fields.append('Номер телефона')

        return empty_fields

    def validate_fullname(self):
        if not self.fullname.replace(' ', '').isalpha():
            raise ValidationException('Имя должно содержать только буквы')
        if len(self.fullname) > 256:
            raise ValidationException('Имя слишком длинное!')
        if len(self.fullname.split()) < 2:
            raise ValidationException('Введите как минимум имя и фамилию!')
        if len(self.fullname.split()) > 5:
            raise ValidationException('Слишком много составных частей имени')
    
    def validate_phone_number(self):
        import re
        pattern = r'^(\+7|8)\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'
        if re.match(pattern, self.phone_number) is None:
            raise ValidationException('Неверный формат номера телефона')
    
    def validate_inn(self):
        if not self.inn.isdigit():
            raise ValidationException('ИНН должен состоять из цифр')

        if len(self.inn) == 10:
            factors = [2, 4, 10, 3, 5, 9, 4, 6, 8]
            control_sum = sum(int(self.inn[i]) * factors[i] for i in range(9))
            control_digit = control_sum % 11 % 10
            if control_digit != int(self.inn[9]):
                raise ValidationException('Не удалось валидировать ИНН для юридического лица')
        elif len(self.inn) == 12:
            factors_1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            factors_2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

            control_sum_1 = sum(int(self.inn[i]) * factors_1[i] for i in range(10))
            control_digit_1 = control_sum_1 % 11 % 10

            control_sum_2 = sum(int(self.inn[i]) * factors_2[i] for i in range(11))
            control_digit_2 = control_sum_2 % 11 % 10
            if not (control_digit_1 == int(self.inn[10]) and control_digit_2 == int(self.inn[11])):
                raise ValidationException('Не удалось валидировать ИНН для физического лица')
        else:
            raise ValidationException('ИНН должен состоять из 10 (для юридического лица) или 12 (для физического лица) цифр')
