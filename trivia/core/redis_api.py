from abc import ABCMeta, abstractmethod


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
