from trivia.models import Keyboard
from requests.models import Response
from abc import ABCMeta, abstractmethod
from typing import Optional


class TelegramApi(metaclass=ABCMeta):
    """
        Интерфейс получение входящих обновлений и отправки сообщений в телеграм
    """

    @abstractmethod
    def get_updates(self, offset: int) -> Response:
        """
            Получение входящего обновления
        """
        pass

    @abstractmethod
    def send_message(self, chat_id: int,
                     text: str,
                     parse_mode: Optional[str] = None,
                     keyboard: Optional[Keyboard] = None) -> None:
        """
            Отправляет текстовое сообщение
        :param chat_id: идентификация чата
        :param text: текст сообщения
        :param parse_mode: режим для форматирования текста сообщения
        :param keyboard: опциональная встроенная клавиатура, которая будет отображаться пользователю
        :return: None
        """
        pass

    @abstractmethod
    def answer_callback_query(self, callback_query_id: str) -> None:
        """
            Метод для отправки ответов на запросы обратного вызова, отправленные со встроенных клавиатур
            Telegram Api documentation ( https://core.telegram.org/bots/api#answercallbackquery ).
        :param callback_query_id: уникальный идентификатор запроса, на который нужно ответить
        :return: None
        """
        pass

    @abstractmethod
    def edit_message(self, chat_id: int, message_id: int, text: str, parse_mode: Optional[str] = None) -> None:
        """
            Метод для редактирования существующего сообщения в истории сообщений, вместо отправления нового сообщения.
            Telegram Api documentation ( https://core.telegram.org/bots/api#editmessagetext )
        :param chat_id: идентификатор чата
        :param message_id: идентификатор сообщения для редактирования
        :param text: новый текст редактируюмого сообщения
        :param parse_mode: режим для форматирования текста сообщения
        :return: None
        """
        pass

