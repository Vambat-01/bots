from typing import Optional, List
from unittest import IsolatedAsyncioTestCase
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
from core.live_redis_api import DoNothingRedisApi
from trivia.bot_config import GameConfig


CHAT_ID_1 = 125
CHAT_ID_2 = 150
TEST_QUESTIONS_PATH = Path("resources/test_questions.json")
GAME_ID = "125"


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
        return dedent_and_strip(f"""
                      NewFakeState: 
                          on_enter: {self.on_enter_is_called}
                   """)

    def __str__(self):
        return self.__repr__()

    def process_message(self, message: Message) -> BotResponse:
        return BotResponse(Message(CHAT_ID_1, "new fake state message response"))

    def process_command(self, command: Command) -> BotResponse:
        return BotResponse(Message(CHAT_ID_1, "text command"))

    def on_enter(self, chat_id) -> Optional[Message]:
        self.on_enter_is_called = True
        return Message(CHAT_ID_1, "text message on_enter")

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
        message = Message(CHAT_ID_1, self.reply_text)
        bot_response = BotResponse(message, new_state=self.next_state)
        return bot_response

    def process_command(self, command: Command) -> BotResponse:
        self.process_command_is_called = True
        message = Message(CHAT_ID_1, self.reply_text)
        bot_response = BotResponse(message, new_state=self.next_state)
        return bot_response

    def on_enter(self, chat_id) -> Optional[Message]:
        return None

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        self.process_callback_query_is_called = True
        message = Message(CHAT_ID_1, self.reply_text)
        bot_response = BotResponse(message, new_state=self.next_state)
        return bot_response


class FakeTelegramApi(TelegramApi):
    def __init__(self, response_bodies: Optional[List[UpdatesResponse]] = None):
        self.sent_messages: List[str] = []
        if response_bodies is None:
            response_bodies = []
        self.response_bodies = response_bodies
        self.answer_callback_query_is_called = False
        self.edit_message_is_called = False
        self.current_response_index = 0

    async def get_updates(self, offset: int) -> UpdatesResponse:
        response = self.response_bodies[self.current_response_index]
        self.current_response_index += 1
        return response

    async def send_message(self,
                           chat_id: int,
                           text: str,
                           parse_mode: Optional[str] = None,
                           keyboard: Optional[Keyboard] = None):
        self.sent_messages.append(text)

    async def answer_callback_query(self, callback_query_id: str) -> None:
        self.answer_callback_query_is_called = True

    async def edit_message(self, chat_id: int, message_id: int, text: str, parse_mode: Optional[str] = None) -> None:
        self.edit_message_is_called = True

    async def set_webhook(self, url: str) -> None:
        pass

    async def delete_webhook(self, drop_pending_updates: bool) -> None:
        pass


class BotTest(IsolatedAsyncioTestCase):
    class CreateInitialState:
        def __init__(self):
            self.state1 = FakeState("user1 for bot")
            self.state2 = FakeState("user2 for bot")
            self.state_index = 0

        def __call__(self):
            if self.state_index == 0:
                self.state_index += 1
                return self.state1
            else:
                return self.state2

    async def check_transition(self, update_type: UpdateType, response_body: Update):
        telegram_api = FakeTelegramApi()
        next_state = NewFakeState()
        state = FakeState("bot message", next_state)
        bot_state_to_dict_bijection = BotStateToDictBijection(_make_state_factory(TEST_QUESTIONS_PATH))
        game_state = Bot.State()
        bot = Bot(telegram_api, DoNothingRedisApi(), lambda: state, bot_state_to_dict_bijection, game_state)
        update = response_body
        await bot.process_update(update)
        expected = {CHAT_ID_1: BotStateLoggingWrapper(next_state)}
        self.assertEqual(expected, bot.state.chat_states)
        self.assertTrue(next_state.on_enter_is_called)
        self.assertEqual(["bot message", "text message on_enter"], telegram_api.sent_messages)
        if update_type == UpdateType.MESSAGE:
            self.assertTrue(state.process_message_is_called)
        elif update_type == UpdateType.COMMAND:
            self.assertTrue(state.process_command_is_called)
        elif update_type == UpdateType.CALLBACK_QUERY:
            self.assertTrue(state.process_callback_query_is_called)
            self.assertTrue(telegram_api.answer_callback_query_is_called)

    async def test_message_state_transition(self):
        update = make_message_update("1", CHAT_ID_1)
        await self.check_transition(UpdateType.MESSAGE, update)

    async def test_command_state_transition(self):
        update = make_message_update("/command", CHAT_ID_1)
        await self.check_transition(UpdateType.COMMAND, update)

    async def test_callback_query_state_transition(self):
        update = make_callback_query_update("2", CHAT_ID_1)
        await self.check_transition(UpdateType.CALLBACK_QUERY, update)

    async def check_command_without_state_transition(self, user_message: str, is_command: bool):
        update = make_message_update(user_message, CHAT_ID_1)
        telegram_api = FakeTelegramApi()
        state = FakeState("bot message")
        bot_state_to_dict_bijection = BotStateToDictBijection(_make_state_factory(TEST_QUESTIONS_PATH))
        game_state = Bot.State()
        bot = Bot(telegram_api, DoNothingRedisApi(), lambda: state, bot_state_to_dict_bijection, game_state)
        await bot.process_update(update)
        expected = {CHAT_ID_1: state}
        self.assertEqual(expected, bot.state.chat_states)
        self.assertEqual(["bot message"], telegram_api.sent_messages)
        if is_command:
            self.assertTrue(state.process_command_is_called)
        else:
            self.assertTrue(state.process_message_is_called)

    async def test_command_without_transition(self):
        await self.check_command_without_state_transition("/command", True)

    async def test_message_without_transition(self):
        await self.check_command_without_state_transition("/command", True)

    async def test_separate_states_for_separate_chats(self):
        """
        В тесте bot.process_updates() вызывается дважды, чтобы передать боту два апдейта. И проверить, что Bot
        сохраняет состояние разных пользователей
        """
        create_initial_state = BotTest.CreateInitialState()
        update1 = make_message_update("user 1", CHAT_ID_1)
        update2 = make_message_update("user 2", CHAT_ID_2)
        telegram_api = FakeTelegramApi()
        bot_state_to_dict_bijection = BotStateToDictBijection(_make_state_factory(TEST_QUESTIONS_PATH))
        game_state = Bot.State()
        bot = Bot(telegram_api, DoNothingRedisApi(), create_initial_state, bot_state_to_dict_bijection, game_state)
        await bot.process_update(update1)
        await bot.process_update(update2)

        expected = {CHAT_ID_1: create_initial_state.state1, CHAT_ID_2: create_initial_state.state2}
        self.assertEqual(expected, bot.state.chat_states)

    def test_bot_saving(self):
        telegram_api = FakeTelegramApi([])
        state_factory = _make_state_factory(TEST_QUESTIONS_PATH)
        in_game_state = _make_in_game_state(state_factory)
        bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
        game_state = Bot.State({125: in_game_state, 150: in_game_state})
        create_initial_state = lambda: in_game_state
        redis_api = DoNothingRedisApi()
        bot1 = Bot(telegram_api, redis_api, create_initial_state, bot_state_to_dict_bijection, game_state)
        bot2 = Bot(telegram_api, redis_api, create_initial_state, bot_state_to_dict_bijection, Bot.State())
        self.assertNotEqual(bot1, bot2)
        encoded = bot1.save()
        json_encoded = json.dumps(encoded, cls=JSONEncoder, ensure_ascii=False)
        json_decoded = json.loads(json_encoded, cls=JSONDecoder)
        bot2.load(json_decoded)
        self.assertEqual(bot1, bot2)


def make_message_update(text: str, chat_id: int) -> Update:
    """
        Создает Telegram update состоящий из одного сообщения. В зависимости от `text` это сообщение представляет собой
        либо сообщение либо команду от пользователя.
    :param text: текст или команда полученные от пользователя
    :param chat_id: идентификатор чата
    :return: json объект
    """
    data = {
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
                "id": chat_id,
                "first_name": "Степан",
                "last_name": "Капуста",
                "username": "степка",
                "type": "private"
            },
            "date": 1603405920,
            "text": text
        }
    }
    message_update = Update.parse_obj(data)
    return message_update


def make_callback_query_update(callback_data: str, chat_id: int) -> Update:
    """
        Создает Telegram update состоящий из одного CallbackQuery.
    :param callback_data: ответ при нажатие на кнопку встроенной клавиатуры
    :param chat_id: идентификатор чата
    :return: json объект
    """
    data = {
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
                    "id": chat_id,
                    "first_name": "Степан",
                    "last_name": "Капуста",
                    "username": "степка",
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
    call_back_query_update = Update.parse_obj(data)
    return call_back_query_update


def _make_state_factory(questions_file_path: Path) -> BotStateFactory:
    storage = JsonQuestionStorage(questions_file_path)
    random = DoNothingRandom()
    state_factory = BotStateFactory(storage, random, GameConfig.make_game_config(1, 1, 1))
    return state_factory


def _make_in_game_state(state_factory: BotStateFactory) -> InGameState:
    questions_list = [Question("7+3", ["10", "11"], 1, Question.Difficulty.EASY, 2),
                      Question("17+3", ["20", "21"], 2, Question.Difficulty.MEDIUM, 2),
                      Question("27+3", ["30", "31"], 3, Question.Difficulty.HARD, 2)
                      ]
    game_state = InGameState.State(questions_list, GAME_ID, 1, 2)
    state = InGameState(state_factory, game_state)
    return state
