from unittest import TestCase
from core.message import Message
from core.command import Command
from trivia.bot_state import GreetingState, IdleState, BotStateFactory
from trivia.question_storage import JsonQuestionStorage
from test.test_utils import DoNothingRandom, make_game_config
from pathlib import Path


class GreetingStateTest(TestCase):
    def test_process_message(self):
        chat_id = 200
        text = "Hi bot"
        user_message = Message(chat_id, text)
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        game_config = make_game_config(1, 1, 1)
        state_factory = BotStateFactory(storage, random, game_config)
        state = GreetingState(state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("<i>&#129417Trivia bot greeting you</i>", message_resp.message.text)
        self.assertEqual(200, message_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 250
        text = "/start"
        user_command = Command(chat_id, text)
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        game_config = make_game_config(1, 1, 1)
        state_factory = BotStateFactory(storage, random, game_config)
        state = GreetingState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>&#129417Trivia bot greeting you. Enter command /start or /help </i>",
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
        game_config = make_game_config(1, 1, 1)
        state_factory = BotStateFactory(storage, random, game_config)
        state = GreetingState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>Something went wrong. Try again</i>", command_resp.message.text)
        self.assertEqual(255, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

