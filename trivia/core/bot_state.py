from abc import ABCMeta, abstractmethod
from trivia.models import Message, Command, CallbackQuery
from typing import Optional
from trivia.bot_state import BotResponse


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

    @abstractmethod
    def on_enter(self, chat_id) -> Optional[Message]:
        """
            Дает BotState возможность отправить сообщение в чат при смене состояния бота для этого чата
            :return: опциональное сообщение для отправки в чат
        """
        pass

    @abstractmethod
    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        """
            Обрабатывает входящий запрос от кнопки на встроенной клавиатуре
        :param callback_query: входящий запрос от кнопки
        :return: ответ бота
        """