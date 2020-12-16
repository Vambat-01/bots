import requests
from trivia.bot_state import BotState, BotResponse, BotStateLoggingWrapper
from trivia.models import Message, Command, Keyboard, CallbackQuery
from requests.models import Response
from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Any
from trivia.utils import log


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

    def send_message(self,
                     chat_id: int,
                     text: str,
                     parse_mode: Optional[str] = None,
                     keyboard: Optional[Keyboard] = None,
                     ) -> None:

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        body = {
            "text": text,
            "chat_id": chat_id
        }
        if parse_mode is not None:
            body["parse_mode"] = parse_mode

        if keyboard is not None:
            body["reply_markup"] = {
                "inline_keyboard": keyboard.as_json()
            }

        response = requests.post(url, json=body)
        log(f"Send message status code: {response.status_code} ")
        if response.status_code != 200:
            log(f"TelegramAPI: Unexpected status code: {response.status_code}. Response body: {response.text}")

    def answer_callback_query(self, callback_query_id: str) -> None:
        url = f"https://api.telegram.org/bot{self.token}/CallbackQuery"
        body = {
            "callback_query_id": callback_query_id
        }
        response = requests.post(url, json=body)
        log(f"TelegramAPI answer_callback_query status code: {response.status_code}")


class Bot:
    """
        Обрабатывает полученные команды и сообщения от пользователя
    """
    def __init__(self, telegram_api: TelegramApi, state: BotState):
        self.telegram_api = telegram_api
        self.state = BotStateLoggingWrapper(state)
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
            self.last_update_id = update["update_id"]
            bot_response = self.process_update(update)
            if bot_response is not None:
                if bot_response.message is not None:
                    self.telegram_api.send_message(bot_response.message.chat_id,
                                                   bot_response.message.text,
                                                   bot_response.message.parse_mode,
                                                   bot_response.message.keyboard
                                                   )

                if bot_response.new_state is not None:
                    new_state: BotState = bot_response.new_state
                    self.state = BotStateLoggingWrapper(new_state)
                    first_message = self.state.on_enter(self._get_chat_id(update))
                    if first_message is not None:
                        self.telegram_api.send_message(first_message.chat_id,
                                                       first_message.text,
                                                       first_message.parse_mode,
                                                       first_message.keyboard
                                                       )

    def process_update(self, update: Dict[str, Any]) -> Optional[BotResponse]:
        if "message" in update:
            chat_id = self._get_chat_id(update)
            message_text = update["message"]["text"]
            log(f"chat_id : {chat_id}. text: {message_text} ")
            if message_text.startswith("/"):
                user_command = Command(chat_id, message_text)
                bot_response: Optional[BotResponse] = self.state.process_command(user_command)
                return bot_response
            else:
                user_message = Message(chat_id, message_text)
                bot_response = self.state.process_message(user_message)
                return bot_response
        elif "callback_query" in update:
            callback_query_id = update["callback_query"]["id"]
            # TODO: message is optional
            chat_id = update["callback_query"]["message"]["chat"]["id"]
            message_text = update["callback_query"]["message"]["text"]
            message = Message(chat_id, message_text)
            callback_query_data = update["callback_query"]["data"]
            callback_query = CallbackQuery(callback_query_data, message)
            self.telegram_api.answer_callback_query(callback_query_id)
            bot_response = self.state.process_callback_query(callback_query)
            return bot_response
        else:
            log("skipping update")
            return None

    def _get_chat_id(self, update: Dict[str, Any]) -> int:
        if "callback_query" in update:
            chat_id = update["callback_query"]["message"]["chat"]["id"]
        else:
            chat_id = update["message"]["chat"]["id"]
        return chat_id


