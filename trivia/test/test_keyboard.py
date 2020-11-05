from unittest import TestCase
from trivia.bot_state import Button, Keyboard, BotResponse, Message


class KeyboardTest(TestCase):
    def test_keyboard_true(self):
        chat_id = 125
        text = "Test question text"
        buttons = [
            [
                Button("A", "back_A")
            ],
            [
                Button("B", "back_B"),
                Button("C", "back_C")
            ]
        ]
        keyboard = Keyboard(buttons)
        response = BotResponse(Message(chat_id, text, "HTML", keyboard))
        self.assertTrue(response.message.keyboard)
        self.assertEqual(2, len(response.message.keyboard.buttons))
        self.assertEqual(1, len(response.message.keyboard.buttons[0]))
        self.assertEqual(2, len(response.message.keyboard.buttons[1]))

    def test_keyboard_none(self):
        chat_id = 125
        text = "Test question text"
        response = BotResponse(Message(chat_id, text, "HTML"))
        self.assertEqual(None, response.message.keyboard)

