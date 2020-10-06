from abc import ABCMeta, abstractmethod


class Message:
    """
        Обрабатывает текстовое  сообщение
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text


class Command:
    """
        Обрабатывает команду боту
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text


class BotResponse:
    """
        Обрабатывает ответ боту
    """
    def __init__(self, message: Message, new_state: "BotState"):
        pass


class BotState(metaclass=ABCMeta):
    """
        Интерфейс состояния бота
    """
    @abstractmethod
    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает текстовое сообщение
        :param message: сообщение от пользователя
        :return: ответ бота
        """
        pass

    @abstractmethod
    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
        :param command: команда от пользователя
        :return: ответ бота
        """
        pass


class EchoState:
    """
        Слушает телеграм
    """

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает сообщение
        :param message: сообщение от пользователя
        :return: ответ бота
        """
        pass

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        pass

