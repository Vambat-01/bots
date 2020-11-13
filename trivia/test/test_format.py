from unittest import TestCase
from trivia import format
from trivia.question_storage import Question
from trivia.utils import dedent_and_strip
from trivia.models import Button, Keyboard
from trivia.bot_state import make_keyboard_for_question


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


class MakeKeyboardForQuestionTest(TestCase):
    def test_two_answers(self):
        buttons = [
            [
                Button("1", "1"),
                Button("2", "2")
            ]
        ]
        expected = Keyboard(buttons)
        actual = make_keyboard_for_question(2)
        self.assertEqual(expected, actual)

    def test_four_answers(self):
        buttons = [
            [
                Button("1", "1"),
                Button("2", "2")
            ],
            [
                Button("3", "3"),
                Button("4", "4")
            ],
        ]
        expected = Keyboard(buttons)
        actual = make_keyboard_for_question(4)
        self.assertEqual(expected, actual)

    def test_five_answers(self):
        buttons_1 = [[Button(str(i + 1), str(i + 1)) for i in range(5)]]
        expected = Keyboard(buttons_1)
        actual = make_keyboard_for_question(5)
        self.assertEqual(expected, actual)

