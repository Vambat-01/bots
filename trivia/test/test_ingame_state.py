from unittest import TestCase
from trivia.models import Message, Command, Button, Keyboard
from trivia.bot_state import IdleState, InGameState, BotStateFactory, BotState, BotResponse
from trivia.question_storage import Question, JsonQuestionStorage
from typing import List, Tuple, Optional
from trivia.utils import dedent_and_strip
from trivia import format


CHAT_ID = 300


class InGameStateTest(TestCase):
    def check_conversation(self,
                           state_factory: BotStateFactory,
                           first_bot_message: Message,
                           conversation: List[Tuple[str, Message]],
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
        self.assertEqual(first_bot_message, message)
        count = 0
        for user_msg, expected_bot_msg in conversation:
            response = state.process_message(Message(chat_id, user_msg))
            count += 1

            if len(conversation) == count:
                expected_response = BotResponse(expected_bot_msg, expected_state)
                self.assertEqual(expected_response, response)
            else:
                expected_response = BotResponse(expected_bot_msg, None)
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
        check_text = format.get_response_for_valid_answer(True, Question("17+3", ["20", "21"], 0))
        self.assertEqual(check_text, message_resp.message.text
            )
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
        check_text = format.get_response_for_valid_answer(False, Question("17+3", ["20", "21"], 0))
        self.assertEqual(dedent_and_strip(check_text), message_resp.message.text
        )
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
        self.assertEqual("<i>I don't understand you. You can enter a number from 1 to 2</i>", message_resp.message.text)
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
        self.assertEqual("<i>The game is over.</i>", command_resp.message.text)
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
        self.assertEqual("<i>Other commands are not available in the game</i>", command_response.message.text)
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
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        check_text = dedent_and_strip(text)
        self.assertEqual(dedent_and_strip(check_text), response.text
        )
        self.assertEqual(295, response.chat_id)

    def test_when_all_user_answers_another_cor(self):
        state_factory = self.create_state_factory()
        keyboard = format.make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_text = dedent_and_strip(text)
        first_bot_message = Message(CHAT_ID, first_bot_text, "HTML", keyboard)
        text_1 = format.get_response_for_valid_answer(True, Question("17+3", ["20", "21"], 0))
        message_1 = Message(CHAT_ID, text_1, "HTML", keyboard)
        text_2 = format.get_response_for_valid_answer(True, Question("27+3", ["30", "31"], 0))
        message_2 = Message(CHAT_ID, text_2, "HTML", keyboard)
        text_3 = format.get_response_for_valid_answer(True, game_score=6)
        message_3 = Message(CHAT_ID, text_3, "HTML", None)
        conversation = [
                ("1", message_1),
                ('1', message_2),
                ("1", message_3)
            ]

        self.check_conversation(
                                state_factory,
                                first_bot_message,
                                conversation,
                                IdleState(state_factory)
                                )

    def test_when_all_user_answers_another_not_cor(self):
        state_factory = self.create_state_factory()
        keyboard = format.make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_text = dedent_and_strip(text)
        first_bot_message = Message(CHAT_ID, first_bot_text, "HTML", keyboard)
        text_1 = format.get_response_for_valid_answer(False, Question("17+3", ["20", "21"], 0))
        message_1 = Message(CHAT_ID, text_1, "HTML", keyboard)
        text_2 = format.get_response_for_valid_answer(False, Question("27+3", ["30", "31"], 0))
        message_2 = Message(CHAT_ID, text_2, "HTML", keyboard)
        text_3 = format.get_response_for_valid_answer(False, game_score=0)
        message_3 = Message(CHAT_ID, text_3, "HTML", None)
        conversation = [
                ("2", message_1),
                ('2', message_2),
                ("2", message_3)
            ]
        self.check_conversation(
                                state_factory,
                                first_bot_message,
                                conversation,
                                IdleState(state_factory)

        )

    def test_when_all_user_answers_another_foo(self):
        state_factory = self.create_state_factory()
        keyboard = format.make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_text = dedent_and_strip(text)
        first_bot_message = Message(CHAT_ID, first_bot_text, "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        conversation = [
                ("foo", message_1)
            ]
        self.check_conversation(
                                state_factory,
                                first_bot_message,
                                conversation,
                                None

        )

    def test_when_all_user_answers_another_second_foo_cor(self):
        state_factory = self.create_state_factory()
        keyboard = format.make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_text = dedent_and_strip(text)
        first_bot_message = Message(CHAT_ID, first_bot_text, "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        text_2 = format.get_number_of_answers_help(2)
        message_2 = Message(CHAT_ID, text_1, "HTML", None)
        text_3 = format.get_response_for_valid_answer(True, Question("17+3", ["20", "21"], 0))
        message_3 = Message(CHAT_ID, text_3, "HTML", keyboard)
        conversation = [
                ("foo", message_1),
                ('foo', message_2),
                ("1", message_3)
            ]
        self.check_conversation(
                                state_factory,
                                first_bot_message,
                                conversation,
                                None
        )

    def test_when_all_user_answers_another_second_foo_not_cor(self):
        state_factory = self.create_state_factory()
        keyboard = format.make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_text = dedent_and_strip(text)
        first_bot_message = Message(CHAT_ID, first_bot_text, "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        text_2 = format.get_number_of_answers_help(2)
        message_2 = Message(CHAT_ID, text_1, "HTML", None)
        text_3 = format.get_response_for_valid_answer(False, Question("17+3", ["20", "21"], 0))
        message_3 = Message(CHAT_ID, text_3, "HTML", keyboard)
        conversation = [
                ("foo", message_1),
                ('foo', message_2),
                ("2", message_3)
            ]
        self.check_conversation(
                                state_factory,
                                first_bot_message,
                                conversation,
                                None

        )

    def test_when_all_user_answers_another_third_foo_not_cor(self):
        state_factory = self.create_state_factory()
        keyboard = format.make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_text = dedent_and_strip(text)
        first_bot_message = Message(CHAT_ID, first_bot_text, "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        text_2 = format.get_number_of_answers_help(2)
        message_2 = Message(CHAT_ID, text_1, "HTML", None)
        text_3 = format.get_response_for_valid_answer(False, Question("17+3", ["20", "21"], 0))
        message_3 = Message(CHAT_ID, text_3, "HTML", keyboard)
        conversation = [
                ("foo", message_1),
                ('6', message_2),
                ("2", message_3)
            ]
        self.check_conversation(
            state_factory,
            first_bot_message,
            conversation,
            None
        )