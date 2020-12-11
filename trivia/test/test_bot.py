from typing import Optional, List, Dict, Any
from unittest import TestCase
from requests.models import Response
from trivia.bot_state import BotState, BotStateLoggingWrapper
from trivia.models import Message, Command, Keyboard, CallbackQuery
from trivia.bot import Bot, TelegramApi
import json
from trivia.bot_state import BotResponse
from enum import Enum

CHAT_ID = 125


class UpdateType(Enum):
    MESSAGE = 1
    COMMAND = 2
    CALLBACK_QUERY = 3


class NewFakeState(BotState):
    """
        Состояние в которое бот перейдет после начального
    """

    def __init__(self):
        self.on_enter_is_called = False

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"""
                      NewFakeState: 
                          on_enter: {self.on_enter_is_called}
                   """

    def __str__(self):
        return self.__repr__()

    def process_message(self, message: Message) -> BotResponse:
        return BotResponse(Message(CHAT_ID, "new fake state message response"))

    def process_command(self, command: Command) -> BotResponse:
        return BotResponse(Message(CHAT_ID, "text command"))

    def on_enter(self, chat_id) -> Optional[Message]:
        self.on_enter_is_called = True
        return Message(CHAT_ID, "text message on_enter")

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        return None


class FakeState(BotState):
    """
        Начальное тестовое состояние
    """
    def __init__(self, reply_text: str, next_state: Optional["BotState"] = None):
        self.reply_text = reply_text
        self.process_message_is_called = False
        self.process_command_is_called = False
        self.process_callback_query_is_called = False
        self.next_state = next_state

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def process_message(self, message: Message) -> BotResponse:
        self.process_message_is_called = True
        message = Message(CHAT_ID, self.reply_text)
        bot_response = BotResponse(message, self.next_state)
        return bot_response

    def process_command(self, command: Command) -> BotResponse:
        self.process_command_is_called = True
        message = Message(CHAT_ID, self.reply_text)
        bot_response = BotResponse(message, self.next_state)
        return bot_response

    def on_enter(self, chat_id) -> Optional[Message]:
        return None

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        self.process_callback_query_is_called = True
        message = Message(CHAT_ID, self.reply_text)
        bot_response = BotResponse(message, self.next_state)
        return bot_response


class FakeTelegramApi(TelegramApi):
    def __init__(self, response_body: Dict[str, Any]):
        self.sent_messages: List[str] = []
        self.response_body = response_body
        self.answer_callback_query_is_called = False

    def get_updates(self, offset: int) -> Response:
        body = json.dumps(self.response_body)
        content = body.encode('utf-8')
        response = Response()
        response.status_code = 200
        response._content = content
        return response

    def send_message(self,
                     chat_id: int,
                     text: str,
                     parse_mode: Optional[str] = None,
                     keyboard: Optional[Keyboard] = None):
        self.sent_messages.append(text)

    def answer_callback_query(self, callback_query_id: str) -> None:
        self.answer_callback_query_is_called = True


class FixTelegramBotTest(TestCase):
    def check_transition(self, update_type: UpdateType, response_body: Dict[str, Any]):
        telegram_api = FakeTelegramApi(response_body)
        next_state = NewFakeState()
        state = FakeState("bot message", next_state)
        bot = Bot(telegram_api, state)
        bot.process_updates()
        self.assertEqual(bot.state, BotStateLoggingWrapper(next_state))
        self.assertTrue(next_state.on_enter(CHAT_ID))
        self.assertEqual(["bot message", "text message on_enter"], telegram_api.sent_messages)
        if update_type == UpdateType.MESSAGE:
            self.assertTrue(state.process_message_is_called)
        elif update_type == UpdateType.COMMAND:
            self.assertTrue(state.process_command_is_called)
        elif update_type == UpdateType.CALLBACK_QUERY:
            self.assertTrue(state.process_callback_query_is_called)
            self.assertTrue(telegram_api.answer_callback_query_is_called)

    def test_message_state_transition(self):
        response = make_message_update("1")
        self.check_transition(UpdateType.MESSAGE, response)

    def test_command_state_transition(self):
        response = make_message_update("/command")
        self.check_transition(UpdateType.COMMAND, response)

    def test_callback_query_state_transition(self):
        response = make_callback_query_update("2")
        self.check_transition(UpdateType.CALLBACK_QUERY, response)

    def check_command_without_state_transition(self, user_message: str, is_command: bool):
        response = make_message_update(user_message)
        telegram_api = FakeTelegramApi(response)
        state = FakeState("bot message")
        bot = Bot(telegram_api, state)
        bot.process_updates()
        self.assertEqual(bot.state, BotStateLoggingWrapper(state))
        self.assertEqual(["bot message"], telegram_api.sent_messages)
        if is_command:
            self.assertTrue(state.process_command_is_called)
        else:
            self.assertTrue(state.process_message_is_called)

    def test_command_without_transition(self):
        self.check_command_without_state_transition("/command", True)

    def test_message_without_transition(self):
        self.check_command_without_state_transition("/command", True)


def make_message_update(text: str) -> Dict[str, Any]:
    """
        Создает Telegram update состоящий из одного сообщения. В зависимости от `text` это сообщение представляет собой
        либо сообщение либо команду от пользователя.
    :param text: текст или команда полученные от пользователя
    :return: json объект
    """
    data = {
        "ok": True,
        "result": [
            {
                "update_id": 675789456,
                "message": {
                    "message_id": 220,
                    "from": {
                        "id": 1379887547,
                        "is_bot": False,
                        "first_name": "Степан",
                        "last_name": "Капуста",
                        "username": "степка",
                        "language_code": "en"
                    },
                    "chat": {
                        "id": 1379887547,
                        "first_name": "Степан",
                        "last_name": "Капуста",
                        "username": "степка",
                        "type": "private"
                    },
                    "date": 1603405920,
                    "text": text
                }
            }
        ]
    }
    return data


def make_callback_query_update(callback_data: str) -> Dict[str, Any]:
    """
        Создает Telegram update состоящий из одного CallbackQuery.
    :param callback_data: ответ при нажатие на кнопку встроенной клавиатуры
    :return: json объект
    """
    data = {
        "ok": True,
        "result": [
            {
                "update_id": 675789456,
                "callback_query": {
                    "id": "5926616425638781715",
                    "from": {
                        "id": 1379887547,
                        "is_bot": False,
                        "first_name": "Степан",
                        "last_name": "Капуста",
                        "username": "степка",
                        "language_code": "en"
                    },
                    "message": {
                        "message_id": 609,
                        "from": {
                            "id": 1162468954,
                            "is_bot": True,
                            "first_name": "easy_programing_bot",
                            "username": "easy_programing_bot"
                        },
                        "chat": {
                            "id": 13798532547,
                            "first_name": "Евгений",
                            "last_name": "Васильев",
                            "username": "zenja09",
                            "type": "private"
                        },
                        "date": 1605131894,
                        "text": "1",
                        "reply_markup": {
                            "inline_keyboard": [
                                [
                                    {
                                        "text": "one",
                                        "callback_data": "back_one"
                                    },
                                    {
                                        "text": "two",
                                        "callback_data": "back_two"
                                    }
                                ],
                                [
                                    {
                                        "text": "three",
                                        "callback_data": "back_three"
                                    },
                                    {
                                        "text": "four",
                                        "callback_data": "back_four"
                                    }
                                ]
                            ]
                        }
                    },
                    "chat_instance": "-3844293030867837600",
                    "data": callback_data
                }
            }
        ]
    }
    return data



