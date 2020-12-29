from unittest import TestCase
from trivia.models import Message, Command, CallbackQuery, MessageEdit
from trivia.bot_state import IdleState, InGameState, BotStateFactory, BotState, BotResponse, make_keyboard_for_question
from trivia.question_storage import Question, JsonQuestionStorage
from typing import List, Tuple, Optional
from trivia.utils import dedent_and_strip
from trivia import format


CHAT_ID = 300
TEST_QUESTIONS_PATH = "resources/test_questions.json"
GAME_ID = "123"


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
        state = InGameState(questions, state_factory, GAME_ID)
        message = state.on_enter(CHAT_ID)
        self.assertEqual(first_bot_message, message)
        count = 0
        for user_msg, expected_bot_msg in conversation:
            response = state.process_message(Message(CHAT_ID, user_msg))
            count += 1

            if len(conversation) == count:
                expected_response = BotResponse(message=expected_bot_msg, new_state=expected_state)
                self.assertEqual(expected_response, response)
            else:
                expected_response = BotResponse(message=expected_bot_msg, new_state=None)
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
        check_text = format.make_message(True, next_question=Question("17+3", ["20", "21"], 0))
        self.assertEqual(check_text, message_resp.message.text)
        self.assertEqual(CHAT_ID, message_resp.message.chat_id)
        self.assertEqual(None, message_resp.new_state)

    def test_process_message_int_not_correct(self):
        text = "2"
        user_message = Message(CHAT_ID, text)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        message_resp = state.process_message(user_message)
        check_text = format.make_message(False, next_question=Question("17+3", ["20", "21"], 0))
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
        state = InGameState(questions, state_factory, GAME_ID)
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
        text = format.make_question("Question", "7+3", ["10", "11"])
        check_text = dedent_and_strip(text)
        self.assertEqual(dedent_and_strip(check_text), response.text
        )
        self.assertEqual(CHAT_ID, response.chat_id)

    def test_callback_query_when_answer_is_correct(self):
        correct_answer = "1"
        prev_message_id = 750
        prev_message = Message(CHAT_ID, correct_answer)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        current_question_id = 0
        data = f"{GAME_ID}.{current_question_id}.{correct_answer}"
        callback_query = CallbackQuery(data, prev_message, prev_message_id)
        callback_query_response = state.process_callback_query(callback_query)

        next_question_id = 1
        expected_message = Message(CHAT_ID,
                                   format.make_message(
                                       1,
                                       next_question=Question("17+3", ["20", "21"], 0)
                                   ),
                                   "HTML",
                                   make_keyboard_for_question(2, GAME_ID, next_question_id)
                                   )
        expected_message_edit = MessageEdit(CHAT_ID,
                                            prev_message_id,
                                            format.make_message(
                                                1,
                                                1,
                                                Question("7+3", ["10", "11"], 0)
                                            ),
                                            "HTML"
                                            )
        expected = BotResponse(expected_message, expected_message_edit)
        self.assertEqual(expected, callback_query_response)

    def test_callback_query_when_game_id_is_not_correct(self):
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        callback_query = _make_callback_query("1879", "0", "1")
        callback_query_response = state.process_callback_query(callback_query)
        self.assertIsNone(None, callback_query_response)

    def test_callback_query_when_len_data_is_not_correct(self):
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        callback_query = _make_callback_query(GAME_ID, "0", "12.42.f")
        callback_query_response = state.process_callback_query(callback_query)
        self.assertIsNone(None, callback_query_response)

    def test_callback_query_when_question_id_is_not_correct(self):
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        callback_query = _make_callback_query(GAME_ID, "15", "1")
        callback_query_response = state.process_callback_query(callback_query)
        self.assertIsNone(None, callback_query_response)

    def test_callback_query_when_answer_is_not_correct(self):
        incorrect_answer = "2"
        prev_message_id = 750
        prev_message = Message(CHAT_ID, incorrect_answer)
        state = _make_in_game_state(TEST_QUESTIONS_PATH)
        current_question_id = 0
        data = f"{GAME_ID}.{current_question_id}.{incorrect_answer}"
        callback_query = CallbackQuery(data, prev_message, prev_message_id)
        callback_query_response = state.process_callback_query(callback_query)

        next_question_id = 1
        expected_message = Message(CHAT_ID,
                                   format.make_message(
                                       2,
                                       next_question=Question("17+3", ["20", "21"], 0)
                                   ),
                                   "HTML",
                                   make_keyboard_for_question(2, GAME_ID, next_question_id)
                                   )
        expected_message_edit = MessageEdit(CHAT_ID,
                                            prev_message_id,
                                            format.make_message(
                                                1,
                                                2,
                                                Question("7+3", ["10", "11"], 0)
                                            ),
                                            "HTML"
                                            )
        expected = BotResponse(expected_message, message_edit=expected_message_edit)
        self.assertEqual(expected, callback_query_response)

    def test_when_all_user_answers_is_correct(self):
        state_factory = self.create_state_factory()
        question_id = 0
        keyboard_1 = make_keyboard_for_question(2, GAME_ID, question_id)
        keyboard_2 = make_keyboard_for_question(2, GAME_ID, question_id + 1)
        keyboard_3 = make_keyboard_for_question(2, GAME_ID, question_id + 2)
        text = format.make_question("Question", "7+3", ["10", "11"])
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard_1)
        text_1 = format.make_message(
            2,
            next_question=Question("17+3", ["20", "21"], 0)
        )
        message_1 = Message(CHAT_ID, text_1, "HTML", keyboard_2)
        text_2 = format.make_message(
            2,
            next_question=Question("27+3", ["30", "31"], 0)
        )
        message_2 = Message(CHAT_ID, text_2, "HTML", keyboard_3)
        text_3 = format.make_message(2, game_score=6)
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
        question_id = 0
        keyboard_1 = make_keyboard_for_question(2, GAME_ID, question_id)
        keyboard_2 = make_keyboard_for_question(2, GAME_ID, question_id + 1)
        keyboard_3 = make_keyboard_for_question(2, GAME_ID, question_id + 2)
        text = format.make_question("Question", "7+3", ["10", "11"], question_id)
        text_1 = format.make_message(
            2,
            next_question=Question("17+3", ["20", "21"], 0)
        )
        text_2 = format.make_message(
            2,
            next_question=Question("27+3", ["30", "31"], 0)
        )
        text_3 = format.make_message(2, None, game_score=0)
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard_1)
        message_1 = Message(CHAT_ID, text_1, "HTML", keyboard_2)
        message_2 = Message(CHAT_ID, text_2, "HTML", keyboard_3)
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
        question_id = 0
        keyboard = make_keyboard_for_question(2, GAME_ID, question_id)
        text = format.make_question("Question", "7+3", ["10", "11"])
        text_1 = format.get_number_of_answers_help(2)
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard)
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

    def test_when_user_answers_is_other_and_is_correct(self):
        state_factory = self.create_state_factory()
        question_id = 0
        keyboard_1 = make_keyboard_for_question(2, GAME_ID, question_id)
        keyboard_2 = make_keyboard_for_question(2, GAME_ID, question_id + 1)
        text = format.make_question("Question", "7+3", ["10", "11"])
        text_1 = format.get_number_of_answers_help(2)
        text_2 = format.get_number_of_answers_help(2)
        text_3 = format.make_message(
            1,
            next_question=Question("17+3", ["20", "21"], 0)
        )
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard_1)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        message_2 = Message(CHAT_ID, text_2, "HTML", None)
        message_3 = Message(CHAT_ID, text_3, "HTML", keyboard_2)
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
        question_id = 0
        keyboard_1 = make_keyboard_for_question(2, GAME_ID, question_id)
        keyboard_2 = make_keyboard_for_question(2, GAME_ID, question_id + 1)
        text = format.make_question("Question", "7+3", ["10", "11"])
        text_1 = format.get_number_of_answers_help(2)
        text_2 = format.get_number_of_answers_help(2)
        text_3 = format.make_message(
            2,
            next_question=Question("17+3", ["20", "21"], 0)
        )
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard_1)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        message_2 = Message(CHAT_ID, text_2, "HTML", None)
        message_3 = Message(CHAT_ID, text_3, "HTML", keyboard_2)
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

    def test_when_all_user_answers_is_different(self):
        state_factory = self.create_state_factory()
        question_id = 0
        keyboard_1 = make_keyboard_for_question(2, GAME_ID, question_id)
        keyboard_2 = make_keyboard_for_question(2, GAME_ID, question_id + 1)
        text = format.make_question("Question", "7+3", ["10", "11"])
        text_1 = format.get_number_of_answers_help(2)
        text_2 = format.get_number_of_answers_help(2)
        text_3 = format.make_message(
            2,
            next_question=Question("17+3", ["20", "21"], 0)
        )
        first_bot_message = Message(CHAT_ID, dedent_and_strip(text), "HTML", keyboard_1)
        message_1 = Message(CHAT_ID, text_1, "HTML", None)
        message_2 = Message(CHAT_ID, text_2, "HTML", None)
        message_3 = Message(CHAT_ID, text_3, "HTML", keyboard_2)
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
    state = InGameState(questions, state_factory, GAME_ID)
    return state


def _make_callback_query(game_id: str, current_question_id: str, message_text: str) -> CallbackQuery:
    user_message = Message(CHAT_ID, message_text)
    message_id = 750
    data = f"{game_id}.{current_question_id}.{message_text}"
    callback_query = CallbackQuery(data, user_message, message_id)
    return callback_query