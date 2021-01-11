import json
from typing import List
from dataclasses import dataclass
from core.question_storage import QuestionStorage


@dataclass
class Question:
    """
        Представляет собой trivia bot  вопрос
        :param text: Текст вопроса, который мы показываем пользователю
        :param answers: Варианты ответов на вопрос, включая правильный
        :param points: Количество очков за правильный ответ
        :param correct_answer: Опциональный правильный ответ. Правильный ответ по умолчаию на все вопросы 1.
    """
    text: str
    answers: List[str]
    points: int
    correct_answer: int = 1


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
