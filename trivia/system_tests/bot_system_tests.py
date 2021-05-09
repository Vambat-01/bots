from typing import Optional, List, Any, Dict
from unittest import IsolatedAsyncioTestCase
import aiohttp
import json
from core.bot_state import BotState
from core.bot_state_logging_wrapper import BotStateLoggingWrapper
from core.message import Message
from core.command import Command
from core.callback_query import CallbackQuery
from core.keyboard import Keyboard
from core.bot import Bot, TelegramApi
import json
from trivia.bot_state import BotResponse
from core.utils import dedent_and_strip
from enum import Enum
from trivia.bot_state import BotStateFactory
from test.test_utils import DoNothingRandom
from trivia.question_storage import JsonQuestionStorage, Question, JSONEncoder, JSONDecoder
from trivia.bijection import BotStateToDictBijection
from trivia.bot_state import InGameState
from trivia.telegram_models import UpdatesResponse, Update
from pathlib import Path

Json = Any


class BotSystemTests(IsolatedAsyncioTestCase):
    async def check_status_code(self, body: Json, expect: int):
        url = "http://localhost:8000"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as request:
                self.assertEqual(request.status, expect)

    async def test_status_code_200(self):
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
        await self.check_status_code(body, 200)

    async def test_status_code_400(self):
        body = {
            "ok": True,
            "result": []
        }
        await self.check_status_code(body, 400)

    async def test_not_text_status_code_400(self):
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
        await self.check_status_code(body, 400)
