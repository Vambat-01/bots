from unittest import TestCase
from trivia.models import Message, Command, CallbackQuery
from trivia.bot_state import IdleState, InGameState, BotStateFactory, BotState, BotResponse, make_keyboard_for_question
from trivia.question_storage import Question, JsonQuestionStorage
from typing import List, Tuple, Optional
from trivia.utils import dedent_and_strip
from trivia import format


CHAT_ID = 300
TEST_QUESTIONS_PATH = "resources/test_questions.json"


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
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state = InGameState(questions, state_factory)
        message = state.on_enter(CHAT_ID)
        self.assertEqual(first_bot_message, message)
        count = 0
        for user_msg, expected_bot_msg in conversation:
            response = state.process_message(Message(CHAT_ID, user_msg))
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

    def test_process_message_int_correct(self):
        text = "1"
        user_message = Message(CHAT_ID, text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        message_resp = state.process_message(user_message)
        check_text = format.get_response_for_valid_answer(True, Question("17+3", ["20", "21"], 0))
        self.assertEqual(check_text, message_resp.message.text
            )
        self.assertEqual(CHAT_ID, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_int_not_correct(self):
        text = "2"
        user_message = Message(CHAT_ID, text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        message_resp = state.process_message(user_message)
        check_text = format.get_response_for_valid_answer(False, Question("17+3", ["20", "21"], 0))
        self.assertEqual(dedent_and_strip(check_text), message_resp.message.text
        )
        self.assertEqual(CHAT_ID, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_another(self):
        text = "1foo"
        user_message = Message(CHAT_ID, text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        message_resp = state.process_message(user_message)
        self.assertEqual("<i>I don't understand you. You can enter a number from 1 to 2</i>", message_resp.message.text)
        self.assertEqual(CHAT_ID, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_command_stop(self):
        text = "/stop"
        user_command = Command(CHAT_ID, text)
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        state_factory = BotStateFactory(storage)
        state = InGameState(questions, state_factory)
        command_resp = state.process_command(user_command)
        self.assertEqual("<i>The game is over.</i>", command_resp.message.text)
        self.assertEqual(CHAT_ID, command_resp.message.chat_id)
        self.assertEqual(IdleState(state_factory), command_resp.new_state)

    def test_process_command_another(self):
        text = "/start"
        user_command = Command(CHAT_ID, text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        command_response = state.process_command(user_command)
        self.assertEqual("<i>Other commands are not available in the game</i>", command_response.message.text)
        self.assertEqual(CHAT_ID, command_response.message.chat_id)
        self.assertEqual(None, command_response.new_state)

    def test_on_enter(self):
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        response = state.on_enter(CHAT_ID)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        check_text = dedent_and_strip(text)
        self.assertEqual(dedent_and_strip(check_text), response.text
        )
        self.assertEqual(CHAT_ID, response.chat_id)

    def test_callback_query_when_answer_is_correct(self):
        message_text = "1"
        user_message = Message(CHAT_ID, message_text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        callback_query = CallbackQuery(message_text, user_message)
        callback_query_response = state.process_callback_query(callback_query)
        answer_text = format.get_response_for_valid_answer(True, Question("17+3", ["20", "21"], 0))
        expected = BotResponse(Message(CHAT_ID, dedent_and_strip(answer_text), "HTML", make_keyboard_for_question(2)))
        self.assertEqual(expected, callback_query_response)

    def test_callback_query_when_answer_is_not_correct(self):
        message_text = "2"
        user_message = Message(CHAT_ID, message_text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        callback_query = CallbackQuery(message_text, user_message)
        callback_query_response = state.process_callback_query(callback_query)
        answer_text = format.get_response_for_valid_answer(False, Question("17+3", ["20", "21"], 0))
        expected = BotResponse(Message(CHAT_ID, dedent_and_strip(answer_text), "HTML", make_keyboard_for_question(2)))
        self.assertEqual(expected, callback_query_response)

    def test_when_all_user_answers_is_correct(self):
        state_factory = self.create_state_factory()
        keyboard = make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
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

    def test_when_all_user_answers_is_not_correct(self):
        state_factory = self.create_state_factory()
        keyboard = make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
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

    def test_when_user_answers_is_foo(self):
        state_factory = self.create_state_factory()
        keyboard = make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
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

    def test_when_user_answers_is_foo_and_is_correct(self):
        state_factory = self.create_state_factory()
        keyboard = make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        text_2 = format.get_number_of_answers_help(2)
        message_2 = Message(CHAT_ID, text_2, "HTML", None)
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

    def test_when_user_answers_is_foo_and_is_not_correct(self):
        state_factory = self.create_state_factory()
        keyboard = make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        text_2 = format.get_number_of_answers_help(2)
        message_2 = Message(CHAT_ID, text_2, "HTML", None)
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

    def test_when_all_user_third_foo_not_correct(self):
        state_factory = self.create_state_factory()
        keyboard = make_keyboard_for_question(2)
        text = format.get_text_questions_answers("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
        text_1 = format.get_number_of_answers_help(2)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        text_2 = format.get_number_of_answers_help(2)
        message_2 = Message(CHAT_ID, text_2, "HTML", None)
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


def _make_in_game_state(questions_file_path: str) -> InGameState:
    """
        Создает InGameState с вопросами из файла questions_file_path
    :param questions_file_path: путь к файлу json
    :return: InGameState
    """
    storage = JsonQuestionStorage(questions_file_path)
    questions = storage.load_questions()
    state_factory = BotStateFactory(storage)
    state = InGameState(questions, state_factory)
    return state


