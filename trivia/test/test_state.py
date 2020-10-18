from unittest import TestCase
from trivia.bot_state import EchoState, Message, Command, BotResponse
from trivia.bot_state import GreetingState, IdleState, InGameState, BotStateFactory, BotState
from trivia.question_storage import Question, JsonQuestionStorage
from typing import List, Tuple, Optional


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
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        state = GreetingState(state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("Trivia bot greeting you", message_resp.message.text)
        self.assertEqual(200, message_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 250
        text = "/start"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        state = GreetingState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("Trivia bot greeting you. Enter command", command_resp.message.text)
        self.assertEqual(250, command_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 255
        text = "start"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        state = GreetingState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("Something went wrong. Try again", command_resp.message.text)
        self.assertEqual(255, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)


class IdleStateTest(TestCase):
    def create_questions(self):
        question_1 = Question("7+3", ["10", "11"], 1)
        question_2 = Question("17+3", ["20", "21"], 2)
        question_3 = Question("27 + 3", ["30", "31"], 3)
        return [question_1, question_2, question_3]

    def test_process_message(self):
        chat_id = 260
        text = "Hello"
        user_message = Message(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        state = IdleState(state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("I did not  understand the command. Enter /start or /help", message_resp.message.text)
        self.assertEqual(260, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_start(self):
        chat_id = 265
        text = "/start"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = IdleState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("Starting game", command_resp.message.text)
        self.assertEqual(265, command_resp.message.chat_id)
        self.assertEqual(InGameState(questions, state_factory), command_resp.new_state)

    def test_process_command_help(self):
        chat_id = 270
        text = "/help"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        state = IdleState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("Enter /start or /help", command_resp.message.text)
        self.assertEqual(270, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 275
        text = "/bla-bla"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        state = IdleState(state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("I did not  understand the command. Enter /start or /help", command_resp.message.text)
        self.assertEqual(275, command_resp.message.chat_id)
        self.assertEqual(None, command_resp.new_state)


class InGameStateTest(TestCase):
    def check_conversation(self,
                           state_factory: BotStateFactory,
                           first_bot_message: str,
                           conversation: List[Tuple[str, str]],
                           expected_state: Optional[BotState] = None):
        """
            Проверяет правильность ответа бота на сообщения и команды от пользователя
            :param state_factory: факбрика состояний, служит для создания состояний бота
            :param first_bot_message: первое сообщение вбота
            :param conversation: список пар (сообщение пользователя, ответ бота на это сообщение)
            :param expected_state: ожидаемое состояние бота в конце диалога
        """
        chat_id = 300
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state = InGameState(questions, state_factory)
        message = state.on_enter(chat_id)
        self.assertEqual(Message(chat_id, first_bot_message), message)
        count = 0
        for user_msg, expected_bot_msg in conversation:
            response = state.process_message(Message(chat_id, user_msg))
            count += 1

            if len(conversation) == count:
                expected_response = BotResponse(Message(chat_id, expected_bot_msg), expected_state)
                self.assertEqual(expected_response, response)
            else:
                expected_response = BotResponse(Message(chat_id, expected_bot_msg), None)
                self.assertEqual(expected_response, response)

    def create_state_factory(self) -> BotStateFactory:
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        return state_factory

    def test_process_message_int_cor(self):
        chat_id = 280
        text = "1"
        user_message = Message(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("Answer is correct! Next question: 17+3", message_resp.message.text)
        self.assertEqual(280, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_int_not_cor(self):
        chat_id = 300
        text = "2"
        user_message = Message(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("Answer is not correct! Next question: 17+3", message_resp.message.text)
        self.assertEqual(300, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_another(self):
        chat_id = 305
        text = "1foo"
        user_message = Message(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        message_resp = state.process_message(user_message)
        self.assertEqual("I don't understand you. You can enter a number from 1 to 2", message_resp.message.text)
        self.assertEqual(305, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_stop(self):
        chat_id = 285
        text = "/stop"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("The game is over.", command_resp.message.text)
        self.assertEqual(285, command_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), command_resp.new_state)

    def test_process_command_another(self):
        chat_id = 290
        text = "/start"
        user_command = Command(chat_id, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        command_response = state.process_command(user_command)
        self.assertEqual("Other commands are not available in the game", command_response.message.text)
        self.assertEqual(290, command_response.message.chat_id)
        self.assertEqual(None, command_response.new_state)

    def test_on_enter(self):
        chat_id = 295
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        response = state.on_enter(chat_id)
        self.assertEqual("Question: 7+3. Choice answer: ['10', '11']", response.text)
        self.assertEqual(295, response.chat_id)

    def test_when_all_user_answers_another_cor(self):
        state_factory = self.create_state_factory()
        conversation = [
                ("1", "Answer is correct! Next question: 17+3"),
                ('1', "Answer is correct! Next question: 27+3"),
                ("1", "Answer is correct! The game is over. Your points: 6")
            ]

        self.check_conversation(
                                state_factory,
                                "Question: 7+3. Choice answer: ['10', '11']",
                                conversation,
                                IdleState(state_factory)
                                )

    def test_when_all_user_answers_another_not_cor(self):
        state_factory = self.create_state_factory()
        conversation = [
                ("2", "Answer is not correct! Next question: 17+3"),
                ('2', "Answer is not correct! Next question: 27+3"),
                ("2", "Answer is not correct! The game is over. Your points: 0")
            ]
        self.check_conversation(
                                state_factory,
                                "Question: 7+3. Choice answer: ['10', '11']",
                                conversation,
                                IdleState(state_factory)

        )

    def test_when_all_user_answers_another_foo(self):
        state_factory = self.create_state_factory()
        conversation = [
                ("foo", "I don't understand you. You can enter a number from 1 to 2")
            ]
        self.check_conversation(
                                state_factory,
                                "Question: 7+3. Choice answer: ['10', '11']",
                                conversation,
                                None

        )

    def test_when_all_user_answers_another_second_foo_cor(self):
        state_factory = self.create_state_factory()
        conversation = [
                ("foo", "I don't understand you. You can enter a number from 1 to 2"),
                ('foo', "I don't understand you. You can enter a number from 1 to 2"),
                ("1", "Answer is correct! Next question: 17+3")
            ]
        self.check_conversation(
                                state_factory,
                                "Question: 7+3. Choice answer: ['10', '11']",
                                conversation,
                                None
        )

    def test_when_all_user_answers_another_second_foo_not_cor(self):
        state_factory = self.create_state_factory()
        conversation = [
                ("foo", "I don't understand you. You can enter a number from 1 to 2"),
                ('foo', "I don't understand you. You can enter a number from 1 to 2"),
                ("2", "Answer is not correct! Next question: 17+3")
            ]
        self.check_conversation(
                                state_factory,
                                "Question: 7+3. Choice answer: ['10', '11']",
                                conversation,
                                None

        )

    def test_when_all_user_answers_another_third_foo_not_cor(self):
        state_factory = self.create_state_factory()
        conversation = [
                ("foo", "I don't understand you. You can enter a number from 1 to 2"),
                ('6', "I don't understand you. You can enter a number from 1 to 2"),
                ("2", "Answer is not correct! Next question: 17+3")
            ]
        self.check_conversation(
            state_factory,
            "Question: 7+3. Choice answer: ['10', '11']",
            conversation,
            None
        )


