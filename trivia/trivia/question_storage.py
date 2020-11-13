import json
from typing import List
from abc import ABCMeta, abstractmethod


class Question:
    """
    Представляет собой trivia bot  вопрос
    """

    def __init__(self, text: str, answers: List[str], points: int):
        """
        :param text: Текст вопроса, который мы показываем пользователю
        :param answers: Варианты ответов на вопрос, включая правильный
        :param points: Количество очков за правильный ответ
        """
        self.text = text
        self.answers = answers
        self.points = points

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class QuestionStorage(metaclass=ABCMeta):
    """
        Интерфейс для доступа к вопросам
    """

    @abstractmethod
    def load_questions(self) -> List[Question]:
        """
            Считывает список вопросов
        :return: список вопросов
        """
        pass


class JsonQuestionStorage(QuestionStorage):
    """
        Класс для чтения вопросов из JSON файла
    """

    def __init__(self, file_path: str):
        """
            Передает путь к файлу
        :param file_path: путь к файлу
        """
        self.file_path = file_path

    def load_questions(self) -> List[Question]:
        """
            Cчитывает список вопросов из файла
        :return: список вопросов
        """
        with open(self.file_path) as json_file:
            data = json.load(json_file)
            questions = []
            for item in data:
                text = item["text"]
                answers = item["answers"]
                points = item["points"]
                quest = Question(text, answers, points)
                questions.append(quest)
            return questions


def main():
    pass


if __name__ == '__main__':
    main()
