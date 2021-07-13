from unittest import TestCase
from core.message import Message
from core.command import Command
from trivia.bot_state import GreetingState, IdleState, BotStateFactory
from trivia.question_storage import JsonQuestionStorage
from test.test_utils import DoNothingRandom
from pathlib import Path
from trivia.bot_config import GameConfig


class GreetingStateTest(TestCase):
    def test_process_message(self):
        chat_id = 200
        text = "Hi bot"
        user_message = Message(chat_id, text)
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random, GameConfig.make(1, 1, 1))
        state = GreetingState(state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("<i>&#129417Умная сова приветствует Вас</i>", message_resp.message.text)
        self.assertEqual(200, message_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 250
        text = "/start"
        user_command = Command(chat_id, text)
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random, GameConfig.make(1, 1, 1))
        state = GreetingState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>&#129417Умная сова приветствует Вас. Введите команду /start или /help </i>",
                         command_resp.message.text
                         )
        self.assertEqual(250, command_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 255
        text = "start"
        user_command = Command(chat_id, text)
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random, GameConfig.make(1, 1, 1))
        state = GreetingState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>Что-то пошло не так. Попробуйте снова</i>", command_resp.message.text)
        self.assertEqual(255, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)
