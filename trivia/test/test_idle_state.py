from unittest import TestCase
from core.message import Message
from core.command import Command
from trivia.bot_state import IdleState, InGameState, BotStateFactory
from trivia.question_storage import JsonQuestionStorage
from typing import cast
from test.test_utils import DoNothingRandom


class IdleStateTest(TestCase):
    def test_process_message(self):
        chat_id = 260
        text = "Hello"
        user_message = Message(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random)
        state = IdleState(state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("<i>I did not  understand the command. Enter /start or /help</i>", message_resp.message.text)
        self.assertEqual(260, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 265
        text = "/start"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random)
        state = IdleState(state_factory)
        command_resp = state.process_command(user_command)
        # game_state = InGameState.State(questions, "125")
        self.assertTrue(isinstance(command_resp.new_state, InGameState))
        new_state = cast(InGameState, command_resp.new_state)
        self.assertEqual("<i>Starting game</i>", command_resp.message.text)
        self.assertEqual(265, command_resp.message.chat_id)
        self.assertEqual(InGameState(questions, state_factory, new_state.game_id),
                         command_resp.new_state)
        # self.assertEqual(InGameState(state_factory, game_state), command_resp.new_state)

    def test_process_command_help(self):
        chat_id = 270
        text = "/help"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random)
        state = IdleState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>Enter /start or /help</i>", command_resp.message.text)
        self.assertEqual(270, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 275
        text = "/bla-bla"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random)
        state = IdleState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>I did not  understand the command. Enter /start or /help</i>", command_resp.message.text)
        self.assertEqual(275, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)
