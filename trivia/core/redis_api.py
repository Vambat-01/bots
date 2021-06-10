from abc import ABCMeta, abstractmethod
from core.bot_state import BotState
from typing import Optional


class RedisApi(metaclass=ABCMeta):
    """
    Интерфейс для доступа к Redis
    """

    @abstractmethod
    async def lock(self, key: str) -> None:
        """
        Получает mutex на ключ
        :param key: ключ
        """
        pass

    @abstractmethod
    def unlock(self, key: str) -> None:
        """
        Убирает mutex на ключ
        :param key: ключ
        """
        pass

    @abstractmethod
    def set_key(self, key: str, value: str):
        """
        Сохраняет состояние бота
        :param key: ключ
        :param value: значение
        """
        pass

    @abstractmethod
    def get_key(self, key: str) -> Optional[str]:
        """
        Получает состояние бота
        :param key: ключ
        :return:  опциональный str
        """
        return None
