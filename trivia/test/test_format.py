from unittest import TestCase
from trivia import format
from trivia.question_storage import Question
from trivia.utils import dedent_and_strip


class GetNumbersOfAnswersHelpTest(TestCase):
    def test_get_number_3(self):
        self.assertEqual("<i>I don't understand you. You can enter a number from 1 to 3</i>",
                         format.get_number_of_answers_help(3)
                         )


class GetResponseForValidAnswerText(TestCase):
    def test_when_answer_is_correct_and_has_next_question(self):
        expected_text = """
                    <i>&#127774 Answer is correct!</i> <b>&#10067Next question:</b>
                        <b>10+10</b>
                    <i>Choose answer:</i>
                    1: 20
                    2: 45
                 """

        self.assertEqual(dedent_and_strip(expected_text),
                         format.get_response_for_valid_answer(True, Question("10+10", ["20", "45"], 0))
                         )

    def test_when_answer_is_not_correct_and_has_next_question(self):
        expected_text = """
                        <i>&#127783 Answer is not correct!</i> <b>&#10067Next question:</b>
                            <b>15+10</b>
                        <i>Choose answer:</i>
                        1: 30
                        2: 28
                     """

        self.assertEqual(dedent_and_strip(expected_text),
                         format.get_response_for_valid_answer(False, Question("15+10", ["30", "28"], 0))
                        )

    def test_when_answer_is_correct_and_score(self):
        expected_text = "<i>&#127774 Answer is correct!</i> <i>The game is over. Your points: 6</i>"
        self.assertEqual(expected_text, format.get_response_for_valid_answer(True, game_score=6))

    def test_when_answer_is_not_correct_and_score(self):
        expected_text = "<i>&#127783 Answer is not correct!</i> <i>The game is over. Your points: 2</i>"
        self.assertEqual(expected_text, format.get_response_for_valid_answer(False, game_score=2))





