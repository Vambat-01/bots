from typing import List, Tuple
from trivia.models import Message, Command, Keyboard, Button, CallbackQuery, MessageEdit
from trivia.question_storage import Question, QuestionStorage
from typing import Optional
from trivia import format
from trivia.utils import log, dedent_and_strip
import uuid
from trivia.random_utils import Random
from core.bot_state import BotState
from core.bot_response import BotResponse


class BotStateFactory:
    """
        Служит для создания состояний бота
    """

    def __init__(self, questions_storage: QuestionStorage, random: Random):
        self.questions_storage = questions_storage
        self.random = random

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"""
                    BotStateFactory: 
                        questions_storage = {self.questions_storage}
                        random = {self.random} 
                """

    def create_idle_state(self):
        """
            Создает IdleState()
        :return: IdleState()
        """

        idle_state = IdleState(self)
        return idle_state

    def create_in_game_state(self):
        """
            Создает InGameState()
        :return: InGameState
        """
        all_questions = self.questions_storage.load_questions()
        game_questions = select_questions(all_questions, 3)
        game_id = str(uuid.uuid4())

        for i in range(len(game_questions)):
            indexed_answers = list(enumerate(game_questions[i].answers))
            self.random.shuffle(indexed_answers)
            correct_answer = 0
            answers = []

            for (index, (original_index, answer)) in enumerate(indexed_answers):
                if original_index == 0:
                    correct_answer = index + 1
                answers.append(answer)

            game_questions[i].answers = answers
            game_questions[i].correct_answer = correct_answer

        in_game_state = InGameState(game_questions, self, game_id)
        return in_game_state


class BotStateLoggingWrapper(BotState):
    def __init__(self, inner: BotState):
        self.inner = inner

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return dedent_and_strip(f"""
                      BotStateLoggingWrapper: 
                          inner: {self.inner}
                   """)

    def __str__(self):
        return self.__repr__()

    def process_message(self, message: Message) -> BotResponse:
        log(f"{type(self.inner).__name__} process_message is called")
        return self.inner.process_message(message)

    def process_command(self, command: Command) -> BotResponse:
        log(f"{type(self.inner).__name__} process_command is called")
        return self.inner.process_command(command)

    def on_enter(self, chat_id: int) -> Optional[Message]:
        log(f"{type(self.inner).__name__} on_enter is called")
        return self.inner.on_enter(chat_id)

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        log(f"{type(self.inner).__name__} callback_query is called")
        return self.inner.process_callback_query(callback_query)


class TestState(BotState):
    """
        Служит для проведения различных тестов, чтобы проверить правильность работы бота. Например, тест на смену
        состояния бота.
    """
    def process_message(self, message: Message) -> BotResponse:
        buttons = [
            [
                Button("A", "back_A"),
                Button("B", "back_B")
            ],
            [
                Button("C", "back_C"),
                Button("D", "back_D")
            ]
        ]
        keyboard = Keyboard(buttons)
        return BotResponse(Message(message.chat_id, "Test Question", "HTML", keyboard))

    def process_command(self, command: Command) -> BotResponse:
        return BotResponse(Message(command.chat_id, command.text))

    def on_enter(self, chat_id: int) -> Optional[Message]:
        return None

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        return None


class EchoState(BotState):
    """
        Обрабатывает полученное сообщение или команду от пользователя и возвращает ответ бота
    """

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает сообщение
        :param message: сообщение от пользователя
        :return: ответ бота
        """
        response_message = Message(message.chat_id, f"I got your message {message.text}")
        response = BotResponse(response_message)
        return response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        response_command = Message(command.chat_id, f"I got your command {command.text}")
        response = BotResponse(response_command)
        return response

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        return None

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Дает BotState возможность отправить сообщение в чат при смене состояния бота для этого чата
            :return: опциональное сообщение для отправки в чат
        """
        return None


class GreetingState(BotState):
    """
        Состояние отвечающее за приветствие пользователя. Первое состоние в котором находится бот
    """

    def __init__(self, state_factory: BotStateFactory):
        self.state_factory = state_factory

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает  сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        idle_state = self.state_factory.create_idle_state()
        response_message = Message(message.chat_id, "<i>&#129417Trivia bot greeting you</i>", "HTML")
        response = BotResponse(message=response_message, new_state=idle_state)
        return response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        idle_state = self.state_factory.create_idle_state()
        command_type = command.text
        if command_type == "/start":
            response_command = Message(command.chat_id,
                                       "<i>&#129417Trivia bot greeting you. Enter command /start or /help </i>",
                                       "HTML"
                                       )
            response = BotResponse(message=response_command, new_state=idle_state)
            return response
        else:
            response_command = Message(command.chat_id, "<i>Something went wrong. Try again</i>")
            response = BotResponse(response_command)
            return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Дает BotState возможность отправить сообщение в чат при смене состояния бота для этого чата
            :return: опциональное сообщение для отправки в чат
        """
        pass

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        return None


class IdleState(BotState):
    """
        Состояние бота после привествия. Служит для обработки команд вне игры
    """

    def __init__(self, state_factory: BotStateFactory):
        self.state_factory = state_factory

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        return f"IdleState.state_factory = {self.state_factory}"

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает  сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        response_message = Message(message.chat_id,
                                   "<i>I did not  understand the command. Enter /start or /help</i>",
                                   "HTML"
                                   )
        response = BotResponse(response_message)
        return response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        new_state = None
        in_game_state = self.state_factory.create_in_game_state()
        user_command = command.text
        if user_command == "/start":
            response_message = Message(command.chat_id, "<i>Starting game</i>", "HTML")
            new_state = in_game_state
        elif user_command == "/help":
            response_message = Message(command.chat_id, "<i>Enter /start or /help</i>", "HTML")
        else:
            response_message = Message(command.chat_id,
                                       "<i>I did not  understand the command. Enter /start or /help</i>",
                                       "HTML"
                                       )
        response = BotResponse(message=response_message, new_state=new_state)
        return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Дает BotState возможность отправить сообщение в чат при смене состояния бота для этого чата
            :return: опциональное сообщение для отправки в чат
        """
        pass

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        return None


class InGameState(BotState):

    def __init__(self, questions: List[Question], state_factory: BotStateFactory, game_id: str):
        self.questions = questions
        self.current_question = 0
        self.game_score = 0
        self.state_factory = state_factory
        self.game_id = game_id

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"""
                    InGameState: 
                        questions = {self.questions}
                        current_questions = {self.current_question} 
                        game_score = {self.game_score}
                        state_factory = {self.state_factory}
                        game_id = {self.game_id}
                """

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        correct_answer = self.questions[self.current_question].correct_answer
        user_message = message.text
        message, new_state = self._process_answer(user_message, message.chat_id, correct_answer)
        return BotResponse(message, new_state=new_state)

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        new_state = None
        idle_state = self.state_factory.create_idle_state()
        user_command = command.text
        if user_command == "/stop":
            response_message = Message(command.chat_id, "<i>The game is over.</i>", "HTML")
            new_state = idle_state
        else:
            response_message = Message(command.chat_id, "<i>Other commands are not available in the game</i>", "HTML")
        response = BotResponse(message=response_message, new_state=new_state)
        return response

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        chat_id = callback_query.message.chat_id
        payload = callback_query.data.split(".")
        message_id = callback_query.message_id

        if len(payload) == 3:
            game_id = payload[0]
            quest_id = self.parse_int(payload[1])

            if quest_id is None:
                return None

            answer_id = payload[2]
            if quest_id >= len(self.questions):
                return None

            correct_answer = self.questions[quest_id].correct_answer

            if game_id == self.game_id and quest_id == self.current_question:
                message, new_state = self._process_answer(answer_id, chat_id, correct_answer)
                message_edit = self._get_message_edit(quest_id, answer_id, correct_answer, chat_id, message_id)
                return BotResponse(message, message_edit=message_edit, new_state=new_state)
        return None

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Возвращает первый вопрос и варианты ответов
            :return: опциональное сообщение для отправки в чат
        """
        quest = self.questions
        first_question = quest[0]
        keyboard = make_keyboard_for_question(len(first_question.answers), self.game_id, self.current_question)
        text = format.make_question("Question",
                                    first_question.text,
                                    first_question.answers,
                                    first_question.correct_answer
                                    )
        message_text = text
        response_message = Message(chat_id, message_text, "HTML", keyboard)
        return response_message

    def parse_int(self, s: str) -> Optional[int]:
        if s.isdigit():
            return int(s)
        return None

    def _process_answer(self,
                        answer: str,
                        chat_id: int,
                        correct_answer: int
                        ) -> Tuple[Message, Optional[BotState]]:
        new_state: Optional[BotState] = None
        num_of_resp = len(self.questions[self.current_question].answers)
        answer_id = self.parse_int(answer)

        if answer_id is None:
            response_message = Message(
                chat_id,
                format.get_number_of_answers_help(num_of_resp),
                "HTML"
            )
        elif answer_id > num_of_resp:
            response_message = Message(
                chat_id,
                format.get_number_of_answers_help(num_of_resp),
                "HTML"
            )
        else:
            if correct_answer == answer_id:
                self.game_score += self.questions[self.current_question].points

            if self.current_question < len(self.questions) - 1:
                next_question = self.questions[self.current_question + 1]
                self.current_question += 1
                keyboard = make_keyboard_for_question(num_of_resp, self.game_id, self.current_question)
                message_text = format.make_message(correct_answer,
                                                   question=next_question
                                                   )
                response_message = Message(chat_id, message_text, "HTML", keyboard)
            else:
                idle_state = self.state_factory.create_idle_state()
                new_state = idle_state
                message_text = format.make_message(1, game_score=self.game_score)
                response_message = Message(chat_id, message_text, "HTML")

        return response_message, new_state

    def _get_message_edit(self, question_id: int,
                          answer_text: Optional[str],
                          correct_answer: int,
                          chat_id: int,
                          message_id: int) -> MessageEdit:
        text_question = self.questions[question_id]
        answer_id = self.parse_int(answer_text) if answer_text is not None else None
        message_text = format.make_message(correct_answer, answer_id, text_question)

        if answer_id == 1:
            return MessageEdit(chat_id,
                               message_id,
                               message_text,
                               "HTML"
                               )

        return MessageEdit(chat_id,
                           message_id,
                           message_text,
                           "HTML"
                           )


def make_keyboard_for_question(num_answers: int, game_id: str, question_id: int) -> Keyboard:
    def button(answer_id: int):
        callback_data = f"{game_id}.{question_id}.{answer_id}"
        return Button(str(answer_id), callback_data)

    if num_answers == 2:
        return Keyboard([[button(1), button(2)]])
    elif num_answers == 4:
        return Keyboard([[button(1), button(2)], [button(3), button(4)]])
    else:
        row = [button(i + 1) for i in range(num_answers)]
        return Keyboard([row])


def select_questions(questions: List[Question], num_questions: int) -> List[Question]:
    """
        Создает List[Questions] из вопросов
        :param questions: вопросы
        :param num_questions: количество вопросов
        :return: Список вопросов
    """
    return questions[:num_questions]


