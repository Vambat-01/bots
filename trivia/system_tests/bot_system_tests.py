from unittest import IsolatedAsyncioTestCase
import aiohttp
from core.utils import Json
from typing import Optional


class BotSystemTests(IsolatedAsyncioTestCase):
    """
    Для запуска тестов, должны быть запущены бот(в режиме server) и redis.
    """
    async def _check_status_code(self, body: Json, expect: int, error_text: Optional[str] = None):
        url = "http://localhost:8000"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as request:
                self.assertEqual(request.status, expect)
                if error_text:
                    request_text = await request.text()
                    self.assertEqual(error_text, request_text)

    async def test_when_request_is_correct(self):
        body = {
            "update_id": 125,
            "message": {
                "message_id": 123,
                "from": {
                    "id": 1379898745,
                    "is_bot": False,
                    "first_name": "Степан",
                    "username": "степка"
                },
                "chat": {
                    "id": 1379898745,
                    "first_name": "Степан",
                    "last_name": "Капуста",
                    "username": "степка",
                    "type": "private"
                },
                "date": 123,
                "text": "1"
            }
        }
        await self._check_status_code(body, 200)

    async def test_when_request_is_not_correct(self):
        body = {
            "ok": True,
            "result": []
        }
        await self._check_status_code(body, 400)

    async def test_when_message_text_is_empty(self):
        body = {
            "update_id": 125,
            "message": {
                "message_id": 123,
                "from": {
                    "id": 1379887547,
                    "is_bot": False,
                    "first_name": "Степан",
                    "username": "степка"
                },
                "chat": {
                    "id": 1379887547,
                    "first_name": "Степан",
                    "last_name": "Капуста",
                    "username": "степка",
                    "type": "private"
                },
                "date": 123
            }
        }
        await self._check_status_code(body, 400)

    async def test_text_error_when_message_text_is_empty(self):
        body = {
            "update_id": 125,
            "message": {
                "message_id": 123,
                "from": {
                    "id": 1379887547,
                    "is_bot": False,
                    "first_name": "Степан",
                    "username": "степка"
                },
                "chat": {
                    "id": 1379887547,
                    "first_name": "Степан",
                    "last_name": "Капуста",
                    "username": "степка",
                    "type": "private"
                },
                "date": 123
            }
        }
        text_error = "Message text is not found"
        await self._check_status_code(body, 400, text_error)

    async def test_when_callback_query_data_is_empty(self):
        body = {
            "update_id": 124,
            "callback_query": {
                "id": "5926616429264821292",
                "from": {
                    "id": 1379897917,
                    "is_bot": False,
                    "first_name": "Степан",
                    "last_name": "Капуста",
                    "username": "степка",
                    "language_code": "en"
                },
                "message": {
                    "message_id": 5386,
                    "from": {
                        "id": 1379887547,
                        "is_bot": True,
                        "first_name": "easy_programing_bot",
                        "username": "easy_programing_bot"
                    },
                    "chat": {
                        "id": 1379887547,
                        "first_name": "Степан",
                        "last_name": "Капуста",
                        "username": "степка",
                        "type": "private"
                    },
                    "date": 1620752261,
                    "text": "🎓 Question:\n    "
                            "Какое количество цветов у радуги?\n"
                            "⚪ 1: Восемь\n"
                            "⚪ 2: Девять\n"
                            "⚪ 3: Пять\n"
                            "⚪ 4: Семь",
                    "entities": [{
                        "offset": 0,
                        "length": 12,
                        "type": "bold"
                    }, {
                        "offset": 17,
                        "length": 33,
                        "type": "bold"
                    }],
                    "reply_markup": {
                        "inline_keyboard": [
                            [{
                                "text": "1",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.1"
                            }, {
                                "text": "2",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.2"
                            }],
                            [{
                                "text": "3",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.3"
                            }, {
                                "text": "4",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.4"
                            }]
                        ]
                    }
                },
                "chat_instance": "-3844293030867837600"
            }
        }
        text_error = "CallbackQuery data is not found"
        await self._check_status_code(body, 400, text_error)

    async def test_when_callback_query_message_text_is_empty(self):
        body = {
            "update_id": 125,
            "callback_query": {
                "id": "5926616429264821292",
                "from": {
                    "id": 1379893456,
                    "is_bot": False,
                    "first_name": "Степан",
                    "last_name": "Капуста",
                    "username": "степка",
                    "language_code": "en"
                },
                "message": {
                    "message_id": 5386,
                    "from": {
                        "id": 1162468954,
                        "is_bot": True,
                        "first_name": "easy_programing_bot",
                        "username": "easy_programing_bot"
                    },
                    "chat": {
                        "id": 1379893456,
                        "first_name": "Степан",
                        "last_name": "Капуста",
                        "username": "степка",
                        "type": "private"
                    },
                    "date": 1620752261,
                    "entities": [{
                        "offset": 0,
                        "length": 12,
                        "type": "bold"
                    }, {
                        "offset": 17,
                        "length": 33,
                        "type": "bold"
                    }],
                    "reply_markup": {
                        "inline_keyboard": [
                            [{
                                "text": "1",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.1"
                            }, {
                                "text": "2",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.2"
                            }],
                            [{
                                "text": "3",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.3"
                            }, {
                                "text": "4",
                                "callback_data": "900168c3-943b-4177-b212-553720ee24d2.0.4"
                            }]
                        ]
                    }
                },
                "chat_instance": "-3844293030867837600",
                "data": "900168c3-943b-4177-b212-553720ee24d2.0.1"
            }
        }
        text_error = "Message text is not found"
        await self._check_status_code(body, 400, text_error)
