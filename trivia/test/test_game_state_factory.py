from unittest import TestCase
from trivia.bot_state import BotStateFactory
from trivia.question_storage import Question, JsonQuestionStorage

from test.test_utils import ReversedShuffleRandom


class BotStateFactoryTest(TestCase):
    def test_answer_shuffling_for_in_game_state(self):
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        random = ReversedShuffleRandom()
        state_factory = BotStateFactory(storage, random)
        actual = state_factory.create_in_game_state()

        questions_list = [Question("7+3", ["11", "10"], 1, 2),
                          Question("17+3", ["21", "20"], 2, 2),
                          Question("27+3", ["31", "30"], 3, 2)
                          ]
        self.assertEqual(questions_list, actual.questions)


