import json
from typing import List
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import sqlite3
from collections import defaultdict


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


class SqliteQuestionStorage(QuestionStorage):
    """
        Класс для чтения вопросов из database SQLite
    """

    @dataclass
    class Record:
        """
            Класс для удобного хранения вопросов из database SQLite
        """
        question_text: str
        points: int
        questions_id: int
        answer_text: str
        is_correct: bool

    def __init__(self, connect: sqlite3.Connection):
        """
            Передает подключение к базе данных
        :param connect: подключение к базе данных
        """
        self.connect = connect

    def load_questions(self) -> List[Question]:
        """
            Считывает список вопросов из базы данных
        :return: список вопросов
        """
        con = self.connect
        cur = con.cursor()
        items = cur.execute("""
                            SELECT t1.text, t1.points, t2.questions_id, t2.text, t2.is_correct
                            FROM questions AS t1 INNER JOIN answers AS t2
                            ON t1.id = t2.questions_id
                            """)

        all_records = [SqliteQuestionStorage.Record(*item) for item in items]

        groups = defaultdict(list)
        for r in all_records:
            groups[r.questions_id].append(r)

        questions = []
        for question_id, records in groups.items():
            text = records[0].question_text
            points = records[0].points
            answers = [r.answer_text for r in records]
            correect_answer_index = [r.is_correct for r in records].index(True)
            questions.append(Question(text, answers, points, correect_answer_index))
        return questions


def main():
    pass


if __name__ == '__main__':
    main()
