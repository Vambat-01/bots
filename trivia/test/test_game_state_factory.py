from unittest import TestCase
from trivia.bot_state import BotStateFactory
from trivia.question_storage import Question, JsonQuestionStorage
from pathlib import Path
from test.test_utils import ReversedShuffleRandom, make_game_config


class BotStateFactoryTest(TestCase):
    def test_answer_shuffling_for_in_game_state(self):
        json_file = Path("resources/test_questions.json")
        storage = JsonQuestionStorage(json_file)
        random = ReversedShuffleRandom()
        game_config = make_game_config(1, 1, 1)
        state_factory = BotStateFactory(storage, random, game_config)
        actual = state_factory.create_in_game_state()

        questions_list = [Question("7+3", ["11", "10"], 1, Question.Difficulty.EASY, 1),
                          Question("17+3", ["21", "20"], 2, Question.Difficulty.MEDIUM, 1),
                          Question("27+3", ["31", "30"], 3, Question.Difficulty.HARD, 1)
                          ]
        self.assertEqual(questions_list, actual.state.questions)
