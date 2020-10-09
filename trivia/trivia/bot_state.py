from abc import ABCMeta, abstractmethod


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


class GreetingState(BotState):
    """
        Приветствует пользователя
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

