from typing import Optional, List
from unittest import TestCase
from requests.models import Response
from trivia.bot_state import EchoState, BotState, Message, Command
from trivia.bot import Bot, TelegramApi
import json
from trivia.bot_state import BotResponse

CHAT_ID = 125


class NewFakeState(BotState):
    """
        Состояние в которое бот перейдет после начального.     проверять on_enter
    """

    def __init__(self, new_state: Optional["BotState"] = None):
        self.new_state = new_state
        self.on_enter_is_called = False

    def process_message(self, message: Message) -> BotResponse:
        return BotResponse(Message(CHAT_ID, "text message"), self.new_state)

    def process_command(self, command: Command) -> BotResponse:
        return BotResponse(Message(CHAT_ID, "text command"), self.new_state)

    def on_enter(self, chat_id) -> Optional[Message]:
        self.on_enter_is_called = True
        return Message(CHAT_ID, "text message on_enter")


class FakeState(BotState):
    """
        Начальное тестовое состояние
    """
    def __init__(self, text: str, new_state: Optional["BotState"] = None):
        self.text = text
        self.process_message_is_called = False
        self.process_command_is_called = False
        self.new_state = new_state

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает текстовое сообщние
        :param message: сообщение от пользователя
        :return: ответ бота
        """
        self.process_message_is_called = True

        message = Message(CHAT_ID, self.text)
        bor_response = BotResponse(message, self.new_state)
        return bor_response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду пользователя
        :param command: команда от пользователя
        :return: ответ бота
        """
        self.process_command_is_called = True
        message = Message(CHAT_ID, self.text)
        bot_response = BotResponse(message, self.new_state)
        return bot_response

    def on_enter(self, chat_id) -> Optional[Message]:
        """
            Дает возможность отправильно сообщение в чат при смене состояние для этого чата
        :param chat_id: идентификатор чата
        :return: опциональное сообщение для отправки в чат
        """
        return None


class FakeTelegramApi(TelegramApi):
    def __init__(self, text: str):
        self.sent_messages: List[str] = []
        self.text = text

    def get_updates(self, offset: int) -> Response:
        data = {
            "ok": True,
            "result": [
                {
                    "update_id": 671149212,
                    "message": {
                        "message_id": 220,
                        "from": {
                            "id": 1379897917,
                            "is_bot": False,
                            "first_name": "Евгений",
                            "last_name": "Васильев",
                            "username": "zenja09",
                            "language_code": "en"
                        },
                        "chat": {
                            "id": 1379897917,
                            "first_name": "Евгений",
                            "last_name": "Васильев",
                            "username": "zenja09",
                            "type": "private"
                        },
                        "date": 1603405920,
                        "text": self.text
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

    def send_message(self, chat_id: int, text: str, parse_mode: Optional[str] = None):
        self.sent_messages.append(text)


class FixTelegramBotTest(TestCase):
    def check_state_transition(self, user_message: str, is_command: bool):
        telegram_api = FakeTelegramApi(user_message)
        new_state = NewFakeState()
        state = FakeState("bot message", new_state)
        bot = Bot(telegram_api, state)
        bot.process_updates()
        self.assertEqual(bot.state, new_state)
        self.assertEqual(True, new_state.on_enter_is_called)
        self.assertEqual(["bot message", "text message on_enter"], telegram_api.sent_messages)
        if is_command:
            self.assertEqual(True, state.process_command_is_called)
        else:
            self.assertEqual(True, state.process_message_is_called)

    def test_command_transition(self):
        self.check_state_transition("/command", True)

    def test_message_transition(self):
        self.check_state_transition("user message", False)

    def check_command_without_state_transition(self, user_message: str, is_command: bool):
        telegram_api = FakeTelegramApi(user_message)
        state = FakeState("bot message")
        bot = Bot(telegram_api, state)
        bot.process_updates()
        self.assertEqual(bot.state, state)
        self.assertEqual(["bot message"], telegram_api.sent_messages)
        if is_command:
            self.assertEqual(True, state.process_command_is_called)
        else:
            self.assertEqual(True, state.process_message_is_called)

    def test_command_without_transition(self):
        self.check_command_without_state_transition("/command", True)

    def test_message_without_transition(self):
        self.check_command_without_state_transition("/command", True)


