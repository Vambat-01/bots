from unittest import TestCase
from core.button import Button
from core.keyboard import Keyboard


class KeyboardTest(TestCase):
    def test_keyboard_json_conversion(self):
        buttons = [
            [
                Button("A", "back_A")
            ],
            [
                Button("B", "back_B"),
                Button("C", "back_C")
            ]
        ]
        expected = [[{'callback_data': 'back_A', 'text': 'A'}],
                   [{'callback_data': 'back_B', 'text': 'B'},
                    {'callback_data': 'back_C', 'text': 'C'}]]
        actual = Keyboard(buttons).as_json()
        self.assertEqual(expected, actual)




