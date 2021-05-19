import json
from unittest import TestCase
from trivia.bot_state import BotStateFactory, GreetingState, IdleState, InGameState
from trivia.question_storage import JsonQuestionStorage
from test.test_utils import DoNothingRandom, make_bot_config
from trivia.bijection import BotStateToDictBijection
from trivia.question_storage import Question
from pathlib import Path


TEST_QUESTIONS_PATH = Path("resources/test_questions.json")
GAME_ID = "125"


class BijectionTest(TestCase):
    def test_greeting_state(self):
        state_factory = _make_state_factory(TEST_QUESTIONS_PATH)
        greeting_state = GreetingState(state_factory)
        bijection = BotStateToDictBijection(state_factory)
        encoded = bijection.forward(greeting_state)
        decoded = bijection.backward(encoded)
        self.assertEqual(greeting_state, decoded)

    def test_idle_state(self):
        state_factory = _make_state_factory(TEST_QUESTIONS_PATH)
        idle_state = IdleState(state_factory)
        bijection = BotStateToDictBijection(state_factory)
        encoded = bijection.forward(idle_state)
        decoded = bijection.backward(encoded)
        self.assertEqual(idle_state, decoded)

    def test_in_game_state(self):
        state_factory = _make_state_factory(TEST_QUESTIONS_PATH)
        in_game_state = _make_in_game_state(state_factory)
        bijection = BotStateToDictBijection(state_factory)
        encoded = bijection.forward(in_game_state)
        decoded = bijection.backward(encoded)
        self.assertEqual(in_game_state, decoded)


def _make_state_factory(questions_file_path: Path) -> BotStateFactory:
    storage = JsonQuestionStorage(questions_file_path)
    random = DoNothingRandom()
    config = make_bot_config(Path("resources/test_config_client.json"))
    state_factory = BotStateFactory(storage, random, config)
    return state_factory


def _make_in_game_state(state_factory: BotStateFactory) -> InGameState:
    questions_list = [Question("7+3", ["10", "11"], 1, Question.Difficulty.EASY, 2),
                      Question("17+3", ["20", "21"], 2, Question.Difficulty.MEDIUM, 2),
                      Question("27+3", ["30", "31"], 3, Question.Difficulty.HARD, 2)
                      ]
    game_state = InGameState.State(questions_list, GAME_ID, 1, 2)
    state = InGameState(state_factory, game_state)
    return state
