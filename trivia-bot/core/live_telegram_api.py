from core.keyboard import Keyboard
from typing import Optional
import logging
from core.telegram_api import TelegramApi
from trivia.telegram_models import UpdatesResponse
import json
import aiohttp
from contextlib import asynccontextmanager
from pathlib import Path


class LiveTelegramApi(TelegramApi):
    def __init__(self, token: str):
        self.token = token
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def get_updates(self, offset: int) -> UpdatesResponse:
        """
            Получает входящее обновление
        :param offset: числовой номер обновления
        :return: Response
        """

        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        logging.info(f"Listen to telegram. offset: {offset}")
        body = {
            "offset": offset,
            "timeout": 10
        }
        response = await self.session.get(url, json=body)
        logging.info(f"Status code get_update {response.status}")
        response_body = await response.text()
        response_json = json.loads(response_body)
        update_data = UpdatesResponse.parse_obj(response_json)
        return update_data

    async def send_message(self,
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

        response = await self.session.post(url, json=body)
        logging.info(f"Send message status code: {response.status} ")
        if response.status != 200:
            response_text = await response.text()
            logging.info(f"TelegramAPI: Unexpected status code: {response.status}. Response body: {response_text}")

    async def answer_callback_query(self, callback_query_id: str) -> None:
        url = f"https://api.telegram.org/bot{self.token}/answerCallbackQuery"
        body = {
            "callback_query_id": callback_query_id
        }
        response = await self.session.post(url, json=body)
        logging.info(f"TelegramAPI answer_callback_query status code: {response.status}")

    async def edit_message(self, chat_id: int, message_id: int, text: str, parse_mode: Optional[str] = None) -> None:
        url = f"https://api.telegram.org/bot{self.token}/editMessageText"
        body = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }
        if parse_mode is not None:
            body["parse_mode"] = parse_mode

        response = await self.session.post(url, json=body)
        logging.info(f"TelegramAPI message_edit status code: {response.status}")

    async def set_webhook(self, https_url: str, cert_filepath: Optional[Path] = None) -> None:
        url = f"https://api.telegram.org/bot{self.token}/setWebhook"
        if not cert_filepath:
            logging.info("Setting hook without certificate")
            body = {
                "url": https_url,
            }
            response = await self.session.post(url, json=body)
        else:
            logging.info(f"Setting hook with certificate from {cert_filepath}")
            with open(cert_filepath, 'r') as cert:
                files = {'certificate': cert, 'url': https_url}
                response = await self.session.post(url, data=files)
        logging.info(f"TelegramAPI set_webhook status code: {response.status}")

    async def delete_webhook(self, drop_pending_updates: bool) -> None:
        url = f"https://api.telegram.org/bot{self.token}/deleteWebhook"
        body = {
            "drop_pending_updates": drop_pending_updates
        }
        response = await self.session.post(url, json=body)
        logging.info(f"TelegramAPI delete_webhook status code: {response.status}")


@asynccontextmanager
async def make_live_telegram_api(token: str):
    telegram = LiveTelegramApi(token)
    try:
        yield telegram
    finally:
        await telegram.close()
