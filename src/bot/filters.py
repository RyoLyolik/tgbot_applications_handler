from aiogram.filters import BaseFilter
from aiogram.types import Message

from validators import States
from utils import get_user


class StatesFilter(BaseFilter):
    def __init__(self, state: States):
        self.state: str | list = state

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.state, str):
            user_id = str(message.from_user.id)
            user = await get_user(user_id)
            return user.state.value == self.state
        if isinstance(self.state, list):
            user_id = str(message.from_user.id)
            user = await get_user(user_id)
            return user.state.value in self.state
        return False
