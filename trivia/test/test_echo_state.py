from unittest import TestCase
from trivia.bot_state import EchoState, Message, Command, GreetingState


class EchoStateTest(TestCase):
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


class GreetingStateTest(TestCase):
    def test_process_message(self):
        user_chat_id = 200
        text = "Hi bot"
        user_message = Message(user_chat_id, text)
        message = GreetingState()
        message_resp = message.process_message(user_message)
        self.assertEqual("Trivia bot greeting you", message_resp.message.text)
        self.assertEqual(200, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_start(self):
        user_chat_id = 250
        text = "/start"
        user_command = Command(user_chat_id, text)
        command = GreetingState()
        command_resp = command.process_command(user_command)
        self.assertEqual("Trivia bot greeting you. Enter command", command_resp.message.text)
        self.assertEqual(250, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_another(self):
        user_chat_id = 255
        text = "start"
        user_command = Command(user_chat_id, text)
        command = GreetingState()
        command_resp = command.process_command(user_command)
        self.assertEqual("Something went wrong. Try again", command_resp.message.text)
        self.assertEqual(255, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)