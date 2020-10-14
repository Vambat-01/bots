from unittest import TestCase
from trivia.bot_state import EchoState, Message, Command, BotResponse
from trivia.bot_state import GreetingState, IdleState, InGameState
from trivia.question_storage import Question
from typing import List, Tuple


class EchoStateTest(TestCase):
    def test_process_message(self):
        chat_id = 100
        text = "Hello"
        user_message = Message(chat_id, text)
        state = EchoState()
        state_resp = state.process_message(user_message)
        self.assertEqual("I got your message Hello", state_resp.message.text)
        self.assertEqual(100, state_resp.message.chat_id)
        self.assertEqual(None, state_resp.new_state)

    def test_process_command(self):
        chat_id = 150
        text = "/start"
        user_command = Command(chat_id, text)
        state = EchoState()
        state_resp = state.process_command(user_command)
        self.assertEqual("I got your command /start", state_resp.message.text)
        self.assertEqual(None, state_resp.new_state)
        self.assertEqual(150, state_resp.message.chat_id)


class GreetingStateTest(TestCase):
    def test_process_message(self):
        chat_id = 200
        text = "Hi bot"
        user_message = Message(chat_id, text)
        state = GreetingState()
        message_resp = state.process_message(user_message)
        self.assertEqual("Trivia bot greeting you", message_resp.message.text)
        self.assertEqual(200, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 250
        text = "/start"
        user_command = Command(chat_id, text)
        state = GreetingState()
        command_resp = state.process_command(user_command)
        self.assertEqual("Trivia bot greeting you. Enter command", command_resp.message.text)
        self.assertEqual(250, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 255
        text = "start"
        user_command = Command(chat_id, text)
        state = GreetingState()
        command_resp = state.process_command(user_command)
        self.assertEqual("Something went wrong. Try again", command_resp.message.text)
        self.assertEqual(255, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)


class ReadyToPlayStateTest(TestCase):
    def test_process_message(self):
        chat_id = 260
        text = "Hello"
        user_message = Message(chat_id, text)
        state = IdleState()
        message_resp = state.process_message(user_message)
        self.assertEqual("I did not  understand the command. Enter /start or /help", message_resp.message.text)
        self.assertEqual(260, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 265
        text = "/start"
        user_command = Command(chat_id, text)
        state = IdleState()
        command_resp = state.process_command(user_command)
        self.assertEqual("Starting game", command_resp.message.text)
        self.assertEqual(265, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_help(self):
        chat_id = 270
        text = "/help"
        user_command = Command(chat_id, text)
        state = IdleState()
        command_resp = state.process_command(user_command)
        self.assertEqual("Enter /start or /help", command_resp.message.text)
        self.assertEqual(270, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 275
        text = "/bla-bla"
        user_command = Command(chat_id, text)
        state = IdleState()
        command_resp = state.process_command(user_command)
        self.assertEqual("I did not  understand the command. Enter /start or /help", command_resp.message.text)
        self.assertEqual(275, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)


class InGameStateTest(TestCase):
    def create_questions(self):
        question_1 = Question("7+3", ["10", "11"], 1)
        question_2 = Question("17+3", ["20", "21"], 2)
        question_3 = Question("27 + 3", ["30", "31"], 3)
        return [question_1, question_2, question_3]

    def check_conversation(self, first_bot_message: str, conversation: List[Tuple[str, str]]):
        chat_id = 300
        questions = self.create_questions()
        state = InGameState(questions)
        message = state.on_enter(chat_id)
        self.assertEqual(Message(chat_id, first_bot_message), message)

        for user_msg, expected_bot_msg in conversation:
            response = state.process_message(Message(chat_id, user_msg))
            self.assertEqual(BotResponse(Message(chat_id, expected_bot_msg)), response)

    def test_process_message_int_cor(self):
        chat_id = 280
        text = "1"
        user_message = Message(chat_id, text)
        questions = InGameStateTest()
        list_quest = questions.create_questions()
        state = InGameState(list_quest)
        message_resp = state.process_message(user_message)
        self.assertEqual("Answer is correct! Next question: 17+3", message_resp.message.text)
        self.assertEqual(280, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_int_not_cor(self):
        chat_id = 300
        text = "3"
        user_message = Message(chat_id, text)
        questions = InGameStateTest()
        list_quest = questions.create_questions()
        state = InGameState(list_quest)
        message_resp = state.process_message(user_message)
        self.assertEqual("Answer is not correct! Next question: 17+3", message_resp.message.text)
        self.assertEqual(300, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_another(self):
        chat_id = 305
        text = "1foo"
        user_message = Message(chat_id, text)
        questions = InGameStateTest()
        list_quest = questions.create_questions()
        state = InGameState(list_quest)
        message_resp = state.process_message(user_message)
        self.assertEqual("I don't understand you. You can enter: 1, 2, 3 or 4", message_resp.message.text)
        self.assertEqual(305, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_stop(self):
        chat_id = 285
        text = "/stop"
        question_1 = Question("7+3", ["10", "11"], 1)
        question_2 = Question("17+3", ["20", "21"], 2)
        user_command = Command(chat_id, text)
        state = InGameState([question_1, question_2])
        command_resp = state.process_command(user_command)
        self.assertEqual("The game is over.", command_resp.message.text)
        self.assertEqual(285, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 290
        text = "/start"
        user_command = Command(chat_id, text)
        questions = InGameStateTest()
        list_quest = questions.create_questions()
        state = InGameState(list_quest)
        command_response = state.process_command(user_command)
        self.assertEqual("Other commands are not available in the game", command_response.message.text)
        self.assertEqual(290, command_response.message.chat_id)
        self.assertEqual(None, command_response.new_state)

    def test_on_enter(self):
        chat_id = 295
        questions = InGameStateTest()
        list_quest = questions.create_questions()
        state = InGameState(list_quest)
        response = state.on_enter(chat_id)
        self.assertEqual("Question: 7+3. Choice answer: ['10', '11']", response.text)
        self.assertEqual(295, response.chat_id)

    def test_when_all_user_answers_another_cor(self):
        self.check_conversation(
            "Question: 7+3. Choice answer: ['10', '11']",
            [
                ("1", "Answer is correct! Next question: 17+3"),
                ('1', "Answer is correct! Next question: 27 + 3"),
                ("1", "Answer is correct! The game is over. Your points: 6")
            ]
        )

    def test_when_all_user_answers_another_not_cor(self):
        self.check_conversation(
            "Question: 7+3. Choice answer: ['10', '11']",
            [
                ("3", "Answer is not correct! Next question: 17+3"),
                ('3', "Answer is not correct! Next question: 27 + 3"),
                ("3", "Answer is not correct! The game is over. Your points: 0")
            ]
        )

    def test_when_all_user_answers_another_foo(self):
        self.check_conversation(
            "Question: 7+3. Choice answer: ['10', '11']",
            [
                ("foo", "I don't understand you. You can enter: 1, 2, 3 or 4"),
            ]
        )