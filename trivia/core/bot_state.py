from abc import ABCMeta, abstractmethod
from core.message import Message
from core.command import Command
from core.callback_query import CallbackQuery
from typing import Optional
from dataclasses import dataclass
from core.message_edit import MessageEdit


@dataclass
class BotResponse:
    """
        Ответ бота
    """
    message: Optional[Message] = None
    message_edit: Optional[MessageEdit] = None
    new_state: Optional["BotState"] = None


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
