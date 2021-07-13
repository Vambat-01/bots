from abc import ABCMeta, abstractmethod
from typing import Optional


class RedisApi(metaclass=ABCMeta):
    """
    Интерфейс для доступа к Redis
    """

    @abstractmethod
    async def lock(self, key: str) -> None:
        """
        Получает mutex на переданный ключ
        """
        pass

    @abstractmethod
    def unlock(self, key: str) -> None:
        """
        Убирает mutex на переданный ключ
        """
        pass

    @abstractmethod
    def set_key(self, key: str, value: str):
        """
        Сохраняет состояние на переданные ключ и значение
        """
        pass

    @abstractmethod
    def get_key(self, key: str) -> Optional[str]:
        """
        Получает состояние на переданные ключ и значение
        """
        return None
