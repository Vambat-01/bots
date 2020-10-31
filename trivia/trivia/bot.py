import requests
import datetime
from trivia.bot_state import Message, Command, BotState
from requests.models import Response
from abc import ABCMeta, abstractmethod
from typing import Optional


def log(message: str) -> None:
    """
        Выводит текущее время и сообщение
    :param message: полученное сообщение
    :return: None
    """
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")


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
    def send_message(self, chat_id: int, text: str, parse_mode: Optional[str] = None) -> None:
        """
            Отправляет текстовое сообщение
        :param chat_id: идентификация чата
        :param text: текст сообщения
        :param parse_mode: режим для форматирования текста сообщения
        :return: None
        """
        pass


class RealTelegramApi(TelegramApi):
    def __init__(self, token: str):
        self.token = token

    def get_updates(self, offset: int) -> Response:
        """
            Получает входящее обновление
        :param offset: числовой номер обновления
        :return: Response
        """
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        log(f"Listen to telegram. offset: {offset}")
        response = requests.get(url, params={
            "offset": offset,
            "timeout": 10
        })
        return response

    def send_message(self, chat_id: int, text: str, parse_mode: Optional[str] = None) -> None:
        """
            Отправляет текстовое сообщение
        :param chat_id: идентификатор чата
        :param text: текст сообщения
        :param parse_mode: режим для форматирования текста сообщения
        :return: None
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.get(url, params={
            "text": text,
            "chat_id": str(chat_id),
            "parse_mode": str(parse_mode)
        })
        log(f"Send message status code: {response.status_code} ")
        if response.status_code != 200:
            log(f"We have a problems: {response.text} ")


class Bot:
    """
        Обрабатывает полученные команды и сообщения от пользователя
    """
    def __init__(self, telegram_api: TelegramApi, state: BotState):
        self.telegram_api = telegram_api
        self.state = state
        self.last_update_id = 0

    def process_updates(self) -> None:
        """
           Обрабатывает полученные команды и сообщения от пользователя
        :return: None
        """
        response = self.telegram_api.get_updates(self.last_update_id + 1)
        data = response.json()
        result = data["result"]
        for update in result:
            chat_id = update["message"]["chat"]["id"]
            message_text = update["message"]["text"]
            log(f"chat_id : {chat_id}. text: {message_text} ")
            if message_text.startswith("/"):
                user_command = Command(chat_id, message_text)
                bot_response = self.state.process_command(user_command)
            else:
                user_message = Message(chat_id, message_text)
                bot_response = self.state.process_message(user_message)
            self.last_update_id = update["update_id"]
            self.telegram_api.send_message(bot_response.message.chat_id,
                                           bot_response.message.text,
                                           bot_response.message.parse_mode
                                           )

            if bot_response.new_state is not None:
                new_state: BotState = bot_response.new_state
                self.state = new_state
                first_message = self.state.on_enter(chat_id)
                if first_message is not None:
                    self.telegram_api.send_message(first_message.chat_id,
                                                   first_message.text,
                                                   bot_response.message.parse_mode
                                                   )



