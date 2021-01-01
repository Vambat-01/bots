from unittest import TestCase
from trivia.bot_state import IdleState, InGameState, BotStateFactory, BotState, BotResponse, make_keyboard_for_question
from trivia.question_storage import Question, JsonQuestionStorage, QuestionStorage
from typing import List, Tuple, Optional
from trivia.utils import dedent_and_strip
from trivia import format
from test.test_utils import ReversedShuffleRandom


class ReversedShuffleRandomTest(TestCase):
    def test_check_revers_answers(self):
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        random = ReversedShuffleRandom()
        state_factory = BotStateFactory(storage, random)
        actual = state_factory.create_in_game_state()

        questions_list = []
        question1 = Question("7+3", ["11", "10"], 1)
        question2 = Question("17+3", ["21", "20"], 2)
        question3 = Question("27+3", ["31", "30"], 3)
        questions_list.append(question1)
        questions_list.append(question2)
        questions_list.append(question3)
        self.assertEqual(questions_list, actual.questions)


