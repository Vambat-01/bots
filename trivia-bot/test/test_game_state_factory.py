from unittest import TestCase
from trivia.bot_state import BotStateFactory
from trivia.question_storage import Question, JsonQuestionStorage
from pathlib import Path
from test.test_utils import ReversedShuffleRandom, DoNothingRandom
from core.bot_exeption import NotEnoughQuestionsException
from trivia.bot_config import GameConfig


class BotStateFactoryTest(TestCase):
    def test_answer_shuffling_for_in_game_state(self):
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = ReversedShuffleRandom()
        state_factory = BotStateFactory(storage, random, GameConfig.make(1, 1, 1))
        actual = state_factory.create_in_game_state()

        questions_list = [Question("7+3", ["11", "10"], 1, Question.Difficulty.EASY, 1),
                          Question("17+3", ["21", "20"], 2, Question.Difficulty.MEDIUM, 1),
                          Question("27+3", ["31", "30"], 3, Question.Difficulty.HARD, 1)
                          ]
        self.assertEqual(questions_list, actual.state.questions)

    def test_answer_shuffling_in_game_state(self):
        json_file = Path("resources/test_questions_for_format.json")
        storage = JsonQuestionStorage(json_file)
        random = ReversedShuffleRandom()
        state_factory = BotStateFactory(storage, random, GameConfig.make(1, 1, 1))
        actual = state_factory.create_in_game_state()

        questions_list = [Question("7+8", ["20", "15", "11", "10"], 1, Question.Difficulty.EASY, 1),
                          Question("27+3", ["30", "25", "21", "20"], 2, Question.Difficulty.MEDIUM, 0),
                          Question("27+4", ["40", "35", "31", "30"], 3, Question.Difficulty.HARD, 2)
                          ]
        self.assertEqual(questions_list, actual.state.questions)

    def test_select_questions(self):
        storage = JsonQuestionStorage(Path("resources/test_questions.json"))
        random = DoNothingRandom()
        state_factory = BotStateFactory(storage, random, GameConfig.make(5, 5, 5))
        with self.assertRaises(NotEnoughQuestionsException) as context:
            state_factory.create_in_game_state()

        self.assertTrue("Not enough questions build a questions list", context.exception)
