from abc import ABCMeta, abstractmethod, ABC
from typing import List
from trivia.question_storage import Question, QuestionStorage
from typing import Optional, Dict, Any
from trivia import format


class Button:
    def __init__(self, text: str, callback_data: str):
        self.text = text
        self.callback_data = callback_data

    def as_json(self) -> Dict[str, str]:
        return {
            "text": self.text,
            "callback_data": self.callback_data
        }


class Keyboard:
    def __init__(self, buttons: List[List[Button]]):
        self.buttons = buttons

    def as_json(self) -> List[Any]:
        res = []
        for button_row in self.buttons:
            row = []
            for button in button_row:
                row.append(button.as_json())
            res.append(row)

        return res


class Message:
    """
        Телеграм сообщение
    """

    def __init__(self, chat_id: int, text: str, parse_mode: Optional[str] = None, keyboad: Optional[Keyboard] = None):
        self.chat_id = chat_id
        self.text = text
        self.parse_mode = parse_mode
        self.keyboard = keyboad

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"""
                    Message:
                    text: {self.text}
                    chat_id: {self.chat_id}
                    parse_mode: {self.parse_mode} 
                 """

    def __str__(self):
        return self.__repr__()


class Command:
    """
        Телеграм команда
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class BotResponse:
    """
        Ответ бота
    """

    def __init__(self, message: Message, new_state: Optional["BotState"] = None):
        self.new_state = new_state
        self.message = message

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"""
                    BotResponse: 
                        new_state: {self.new_state}
                        message: {self.message}                        
                 """

    def __str__(self):
        return self.__repr__()


class BotStateFactory:
    """
        Служит для создания состояний бота
    """

    def __init__(self, questions_storage: QuestionStorage):
        self.questions_storage = questions_storage

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
        list_questions = select_questions(all_questions, 3)
        in_game_state = InGameState(list_questions, self)
        return in_game_state


class BotState(metaclass=ABCMeta):
    """
        Интерфейс состояния бота
    """

    @abstractmethod
    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает текстовое сообщение
        :param message: сообщение от пользователя
        :return: ответ бота
        """
        pass

    @abstractmethod
    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
        :param command: команда от пользователя
        :return: ответ бота
        """
        pass

    @abstractmethod
    def on_enter(self, chat_id) -> Optional[Message]:
        """
            Дает BotState возможность отправить сообщение в чат при смене состояния бота для этого чата
            :return: опциональное сообщение для отправки в чат
        """
        pass


class TestState(BotState):
    def process_message(self, message: Message) -> BotResponse:
        buttons = [
            [
                Button("Button A", "data A"),
                Button("Button B", "data B"),
                Button("Button C", "data C")
            ],
            [
                Button("Button D", "data D"),
                Button("Button E", "data E")
            ]
        ]
        keyboard = Keyboard(buttons)
        return BotResponse(Message(message.chat_id, "Text with a keyboard", "HTML", keyboard))

    def process_command(self, command: Command) -> BotResponse:
        return BotResponse(Message(command.chat_id, command.text))

    def on_enter(self, chat_id: int) -> Optional[Message]:
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
        response = BotResponse(response_message, idle_state)
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
            response = BotResponse(response_command, idle_state)
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
        response = BotResponse(response_message, new_state)
        return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Дает BotState возможность отправить сообщение в чат при смене состояния бота для этого чата
            :return: опциональное сообщение для отправки в чат
        """
        pass


class InGameState(BotState):

    def __init__(self, questions: List[Question], state_factory: BotStateFactory):
        self.questions = questions
        self.current_question = 0
        self.game_score = 0
        self.state_factory = state_factory

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        return f"""
            InGameState: 
                questions = {self.questions}
                current_questions = {self.current_question} 
                game_score = {self.game_score}
                state_factory = {self.state_factory}
        """

    def __repr__(self):
        return self.__str__()

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        new_state = None
        idle_state = self.state_factory.create_idle_state()
        user_message = message.text
        answer_id = self.parse_int(user_message)
        num_of_resp = len(self.questions[self.current_question].answers)
        if answer_id is None:
            response_message = Message(
                message.chat_id,
                format.get_number_of_answers_help(num_of_resp),
                "HTML"
            )
        elif int(user_message) > num_of_resp:
            response_message = Message(
                message.chat_id,
                format.get_number_of_answers_help(num_of_resp),
                "HTML"
            )
        else:
            is_answer_correct = answer_id == 1
            if is_answer_correct:
                self.game_score += self.questions[self.current_question].points

            if self.current_question < len(self.questions) - 1:
                next_question = self.questions[self.current_question + 1]
                self.current_question += 1
                message_text = format.get_response_for_valid_answer(is_answer_correct, next_question=next_question)
            else:
                new_state = idle_state
                message_text = format.get_response_for_valid_answer(is_answer_correct, game_score=self.game_score)

            response_message = Message(message.chat_id, message_text, "HTML")

        response = BotResponse(response_message, new_state)
        return response

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
        response = BotResponse(response_message, new_state)
        return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Возвращает первый вопрос и варианты ответов
            :return: опциональное сообщение для отправки в чат
        """
        quest = self.questions
        first_question = quest[0]

        string_text = format.get_text_questions_answers("Question", first_question.text, first_question.answers)
        message_text = string_text
        response_message = Message(chat_id, message_text, "HTML")
        return response_message

    def parse_int(self, s: str) -> Optional[int]:
        if s.isdigit():
            return int(s)
        return None


def select_questions(questions: List[Question], num_questions: int) -> List[Question]:
    """
        Создает List[Questions] из трех первых вопросов
        :param questions: вопросы
        :param num_questions: количество вопросов
        :return: Список вопросов
    """
    return questions[:num_questions]






