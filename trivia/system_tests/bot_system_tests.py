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
                    self.assertEqual(request_text, error_text)



    # async def _check_status_code(self, body: Json, expect: int):
    #     url = "http://localhost:8000"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(url, json=body) as request:
    #             self.assertEqual(request.status, expect)

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

    async def test_text_error_when_message_is_empty(self):
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
