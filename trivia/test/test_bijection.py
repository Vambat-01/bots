from unittest import TestCase
from trivia.bot_state import BotStateFactory, GreetingState, IdleState, InGameState
from trivia.question_storage import JsonQuestionStorage
from test.test_utils import DoNothingRandom
from trivia.bijection import BotStateToDictBijection


TEST_QUESTIONS_PATH = "resources/test_questions.json"


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
        questions = state_factory.questions_storage.load_questions()
        in_game_state = InGameState(questions, state_factory, "125")
        bijection = BotStateToDictBijection(_make_state_factory(TEST_QUESTIONS_PATH))
        encoded = bijection.forward(in_game_state)
        decoded = bijection.backward(encoded)
        self.assertEqual(in_game_state, decoded)


def _make_state_factory(questions_file_path: str) -> BotStateFactory:
    storage = JsonQuestionStorage(questions_file_path)
    random = DoNothingRandom()
    state_factory = BotStateFactory(storage, random)
    return state_factory
