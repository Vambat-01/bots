from typing import Optional, List
from unittest import TestCase
from requests.models import Response
from trivia.bot_state import BotState, Message, Command, Keyboard
from trivia.bot import Bot, TelegramApi
import json
from trivia.bot_state import BotResponse

CHAT_ID = 125


class NewFakeState(BotState):
    """
        Состояние в которое бот перейдет после начального
    """

    def __init__(self):
        self.on_enter_is_called = False

    def process_message(self, message: Message) -> BotResponse:
        return BotResponse(Message(CHAT_ID, "new fake state message response"))

    def process_command(self, command: Command) -> BotResponse:
        return BotResponse(Message(CHAT_ID, "text command"))

    def on_enter(self, chat_id) -> Optional[Message]:
        self.on_enter_is_called = True
        return Message(CHAT_ID, "text message on_enter")


class FakeState(BotState):
    """
        Начальное тестовое состояние
    """
    def __init__(self, reply_text: str, next_state: Optional["BotState"] = None):
        self.reply_text = reply_text
        self.process_message_is_called = False
        self.process_command_is_called = False
        self.next_state = next_state

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


class FakeTelegramApi(TelegramApi):
    def __init__(self, user_message_text: str):
        self.sent_messages: List[str] = []
        self.user_message_text = user_message_text

    def get_updates(self, offset: int) -> Response:
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
                            "first_name": "Евгений",
                            "last_name": "Васильев",
                            "username": "zenja09",
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
                        "text": self.user_message_text
                    }
                }
            ]
        }
        string = json.dumps(data)
        content = string.encode('utf-8')

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


class FixTelegramBotTest(TestCase):
    def check_state_transition(self, user_message: str, is_command: bool):
        telegram_api = FakeTelegramApi(user_message)
        next_state = NewFakeState()
        state = FakeState("bot message", next_state)
        bot = Bot(telegram_api, state)
        bot.process_updates()
        self.assertEqual(bot.state, next_state)
        self.assertTrue(next_state.on_enter_is_called)
        self.assertEqual(["bot message", "text message on_enter"], telegram_api.sent_messages)
        if is_command:
            self.assertTrue(state.process_command_is_called)
        else:
            self.assertTrue(state.process_message_is_called)

    def test_command_state_transition(self):
        self.check_state_transition("/command", True)

    def test_message_state_transition(self):
        self.check_state_transition("user message", False)

    def check_command_without_state_transition(self, user_message: str, is_command: bool):
        telegram_api = FakeTelegramApi(user_message)
        state = FakeState("bot message")
        bot = Bot(telegram_api, state)
        bot.process_updates()
        self.assertEqual(bot.state, state)
        self.assertEqual(["bot message"], telegram_api.sent_messages)
        if is_command:
            self.assertTrue(state.process_command_is_called)
        else:
            self.assertTrue(state.process_message_is_called)

    def test_command_without_transition(self):
        self.check_command_without_state_transition("/command", True)

    def test_message_without_transition(self):
        self.check_command_without_state_transition("/command", True)


