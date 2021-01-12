from unittest import TestCase
from trivia import format
from trivia.question_storage import Question
from core.utils import dedent_and_strip
from core.button import Button
from core.keyboard import Keyboard
from trivia.bot_state import make_keyboard_for_question


class GetNumbersOfAnswersHelpTest(TestCase):
    def test_get_number_3(self):
        self.assertEqual("<i>I don't understand you. You can enter a number from 1 to 3</i>",
                         format.get_number_of_answers_help(3)
                         )


class GetResponseForValidAnswerText(TestCase):
    def test_when_answer_is_correct_and_has_next_question(self):
        expected_text = """
                    <b>&#127891 Next question:</b>
                        <b>10+10</b>
                    |&#8195| 1: 20
                    |&#8195| 2: 45
                 """

        self.assertEqual(dedent_and_strip(expected_text),
                         format.make_message(True, None, Question("10+10", ["20", "45"], 0))
                         )

    def test_when_answer_is_not_correct_and_has_next_question(self):
        expected_text = """
                        <b>&#127891 Next question:</b>
                            <b>15+10</b>
                        |&#8195| 1: 30
                        |&#8195| 2: 28
                     """

        self.assertEqual(dedent_and_strip(expected_text),
                         format.make_message(False, question=Question("15+10", ["30", "28"], 0))
                         )

    def test_when_answer_is_correct_and_score(self):
        expected_text = "<i>The game is over. Your points: 6</i>"
        self.assertEqual(expected_text, format.make_message(True, game_score=6))

    def test_when_answer_is_not_correct_and_score(self):
        expected_text = "<i>The game is over. Your points: 2</i>"
        self.assertEqual(expected_text, format.make_message(False, game_score=2))


class MakeKeyboardForQuestionTest(TestCase):
    def test_two_answers(self):
        buttons = [
            [
                Button("1", "123.0.1"),
                Button("2", "123.0.2")
            ]
        ]
        expected = Keyboard(buttons)
        game_id = "123"
        question_id = 0
        actual = make_keyboard_for_question(2, game_id, question_id)
        self.assertEqual(expected, actual)

    def test_four_answers(self):
        buttons = [
            [
                Button("1", "123.0.1"),
                Button("2", "123.0.2")
            ],
            [
                Button("3", "123.0.3"),
                Button("4", "123.0.4")
            ],
        ]
        expected = Keyboard(buttons)
        game_id = "123"
        question_id = 0
        actual = make_keyboard_for_question(4, game_id, question_id)
        self.assertEqual(expected, actual)

    def test_five_answers(self):
        buttons_1 = [[Button(str(i + 1), str(f"123.0.{i + 1}")) for i in range(5)]]
        expected = Keyboard(buttons_1)
        game_id = "123"
        question_id = 0
        actual = make_keyboard_for_question(5, game_id, question_id)
        self.assertEqual(expected, actual)
