import requests
from core.keyboard import Keyboard
from typing import Optional
from core.utils import log
from core.telegram_api import TelegramApi
from trivia.parsing_update import UpdateData
import json


class LiveTelegramApi(TelegramApi):
    def __init__(self, token: str):
        self.token = token

    def get_updates(self, offset: int) -> UpdateData:
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
        response_text = json.loads(response.text)
        update_data = UpdateData.from_dict(response_text)   # type: ignore

        return update_data

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
        url = f"https://api.telegram.org/bot{self.token}/answerCallbackQuery"
        body = {
            "callback_query_id": callback_query_id
        }
        response = requests.post(url, json=body)
        log(f"TelegramAPI answer_callback_query status code: {response.status_code}")

    def edit_message(self, chat_id: int, message_id: int, text: str, parse_mode: Optional[str] = None) -> None:
        url = f"https://api.telegram.org/bot{self.token}/editMessageText"
        body = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }
        if parse_mode is not None:
            body["parse_mode"] = parse_mode

        response = requests.post(url, json=body)
        log(f"TelegramAPI message_edit status code: {response.status_code}")
