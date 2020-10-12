from abc import ABCMeta, abstractmethod
from typing import List
from trivia.question_storage import Question
from typing import Optional


class Message:
    """
        Телеграм сообщение
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text


class Command:
    """
        Телеграм команда
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text


class BotResponse:
    """
        Ответ бота
    """
    def __init__(self, message: Message, new_state: "BotState" = None):
        self.new_state = new_state
        self.message = message


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

            :return: ответ бота
        """
        pass


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

            :return: ответ бота
        """
        pass


class GreetingState(BotState):
    """
        Состояние отвечающее за приветствие пользователя. Первое состоние в котором находится бот
    """
    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает  сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        response_message = Message(message.chat_id, "Trivia bot greeting you")
        response = BotResponse(response_message)
        return response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        command_type = command.text
        if command_type == "/start":
            response_command = Message(command.chat_id, "Trivia bot greeting you. Enter command")
            response = BotResponse(response_command)
            return response
        else:
            response_command = Message(command.chat_id, "Something went wrong. Try again")
            response = BotResponse(response_command)
            return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Возвращает первый вопрос и варианты ответов
            :return: ответ бота
        """
        pass


class IdleState(BotState):
    """
        Состояние бота после привествия. Служит для обработки команд вне игры
    """
    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает  сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        response_message = Message(message.chat_id, "I did not  understand the command. Enter /start or /help")
        response = BotResponse(response_message)
        return response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        user_command = command.text
        if user_command == "/start":
            response_message = Message(command.chat_id, "Starting game")
        elif user_command == "/help":
            response_message = Message(command.chat_id, "Enter /start or /help")
        else:
            response_message = Message(command.chat_id, "I did not  understand the command. Enter /start or /help")
        response = BotResponse(response_message)
        return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """

            :return: ответ бота
        """
        pass


class InGameState(BotState):

    def __init__(self, questions: List[Question] ):
        self.questions = questions

    def process_message(self, message: Message) -> BotResponse:
        """
            Обрабатывает сообщение
            :param message: сообщение от пользователя
            :return: ответ бота
        """
        quest = self.questions
        second_question = quest[1]
        user_message = message.text
        answer_id = self.parse_int(user_message)
        if answer_id == 1:
            response_message = Message(message.chat_id, f"Answer is correct! Next question: {second_question.text}")
        elif answer_id is not None and answer_id != 1:
            response_message = Message(message.chat_id, f"Answer is not correct! Next question: {second_question.text}")
        else:
            response_message = Message(message.chat_id, "I don't understand you. You can enter: 1, 2, 3 or 4")
        response = BotResponse(response_message)
        return response

    def process_command(self, command: Command) -> BotResponse:
        """
            Обрабатывает команду
            :param command: команда от пользователя
            :return: ответ бота
        """
        user_command = command.text
        if user_command == "/stop":
            response_message = Message(command.chat_id, "The game is over.")
        else:
            response_message = Message(command.chat_id, "Other commands are not available in the game")
        response = BotResponse(response_message)
        return response

    def on_enter(self, chat_id: int) -> Optional[Message]:
        """
            Возвращает первый вопрос и варианты ответов
            :return: ответ бота
        """
        quest = self.questions
        first_question = quest[0]
        response_message = Message(chat_id, f"Question: {first_question.text}. Choice answer: {first_question.answers}")
        return response_message

    def parse_int(self, s: str) -> Optional[int]:
        if s.isdigit():
            return int(s)


def select_questions(questions: List[Question], num_questions: int) -> List[Question]:
    """
        Создает List[Questions] из трех первых вопросов
        :param questions: вопросы
        :param num_questions: количество вопросов
        :return: Список вопросов
    """
    return questions[:num_questions]


