from abc import ABCMeta, abstractmethod


class RedisApi(metaclass=ABCMeta):
    """
    Интерфейс для доступа к Redis
    """

    @abstractmethod
    async def lock_chat(self, chat_id: int) -> None:
        """
        Получает mutex на чат
        :param chat_id: идентификация чата
        """
        pass

    @abstractmethod
    def unlock_chat(self, chat_id: int) -> None:
        """
        Удаляет один или несколько ключей
        :param chat_id: идентификацикация чата
        """
