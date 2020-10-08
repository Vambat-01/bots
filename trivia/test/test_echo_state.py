import unittest
from trivia.bot_state import EchoState, Message, Command


class EchoStateTest(unittest.TestCase):
    def test_process_message(self):
        user_chat_id = 100
        text = "Hello"
        user_message = Message(user_chat_id, text)
        state = EchoState()
        state_resp = state.process_message(user_message)
        self.assertEqual("I got your message Hello", state_resp.message.text)
        self.assertEqual(100, state_resp.message.chat_id)
        self.assertEqual(None, state_resp.new_state)

    def test_process_command(self):
        user_chat_id = 150
        text = "/start"
        user_command = Command(user_chat_id, text)
        state = EchoState()
        state_resp = state.process_command(user_command)
        self.assertEqual("I got your command /start", state_resp.message.text)
        self.assertEqual(None, state_resp.new_state)
        self.assertEqual(150, state_resp.message.chat_id)