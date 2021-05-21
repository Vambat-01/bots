from abc import ABCMeta, abstractmethod
from core.bot_state import BotState
from typing import Optional


class RedisApi(metaclass=ABCMeta):
    """
    Интерфейс для доступа к Redis
    """

    @abstractmethod
    async def lock_chat(self, chat_id: int) -> None:
        """
        Получает mutex на чат
        :param chat_id: идентификатор чата
        """
        pass

    @abstractmethod
    def unlock_chat(self, chat_id: int) -> None:
        """
        Убирает mutex на чат
        :param chat_id: идентификатор чата
        """
        pass

    @abstractmethod
    def set_state(self, chat_id: str, state: str):
        """
        Сохраняет состояние бота в Redis
        :param chat_id: идентификатор чата
        :param state: состояние бота
        """
        pass

    @abstractmethod
    def get_state(self, chat_id: str) -> Optional[str]:
        """
        Получает состояние бота из Redis
        :param chat_id: идентификатор чата
        :return:  опциональное состояние бота
        """
        pass
