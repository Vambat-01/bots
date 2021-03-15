import json
from typing import List
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import sqlite3
from collections import defaultdict


@dataclass(frozen=True)
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

    def normalize(self) -> "Question":
        """
            Создает эквивалентный вопрос, но с отсортированными по алфавиту ответами
        :return: отсортированный Question
        """
        check_ans = self.answers[self.correct_answer]
        norm_answers = sorted(self.answers)
        norm_correct_answer = norm_answers.index(check_ans)

        return Question(self.text, norm_answers, self.points, norm_correct_answer)


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
        Класс для чтения вопросов из SQLite базы данных
    """

    @dataclass(frozen=True)
    class Record:
        """
            Класс для удобного хранения вопроса из database SQLite
        """
        question_text: str
        points: int
        question_id: int
        answer_text: str
        is_correct: bool

    @staticmethod
    def create_in_memory():
        """
        Создает создает SQLiteQuestionStorage с базой в памяти. В базе присутствует все необходимые таблицы,
        но они не заполнены
        :return:
        """
        connection = sqlite3.connect(":memory:")
        cur = connection.cursor()
        cur.executescript("""
                                    CREATE TABLE questions (
                                    id INTEGER PRIMARY KEY,
                                    text TEXT,
                                    points INTEGER NOT NULL
                                    );

                                    CREATE TABLE answers (
                                    id INTEGER,
                                    questions_id INTEGER NOT NULL,
                                    text TEXT NOT NULL,
                                    is_correct INTEGER NOT NULL,
                                    FOREIGN KEY(questions_id) REFERENCES questions (id))
                                    """)
        storage = SqliteQuestionStorage(connection)
        return storage

    def __init__(self, connection: sqlite3.Connection):
        """
        :param connection: подключение к базе данных
        """
        self.connect = connection

    def load_questions(self) -> List[Question]:
        """
            Считывает список вопросов из базы данных
        :return: список вопросов
        """
        cur = self.connect.cursor()
        items = cur.execute("""
                            SELECT t1.text, t1.points, t2.questions_id, t2.text, t2.is_correct
                            FROM questions AS t1 INNER JOIN answers AS t2
                            ON t1.id = t2.questions_id
                            """)

        all_records = [SqliteQuestionStorage.Record(*item) for item in items]

        groups = defaultdict(list)
        for r in all_records:
            groups[r.question_id].append(r)

        questions = []
        for question_id, records in groups.items():
            text = records[0].question_text
            points = records[0].points
            answers = [r.answer_text for r in records]

            correect_answer_index = [r.is_correct for r in records].index(True)

            questions.append(Question(text, answers, points, correect_answer_index))
        return questions

    def add_questions(self, questions: List[Question]):
        """
            Добавляет вопросы questions  в базу
        :param questions: Список вопросов
        """
        cur = self.connect.cursor()
        question_ids = []
        for quest in questions:
            cur.execute("INSERT INTO questions(text, points) VALUES(?, ?)",
                        (quest.text, quest.points))
            self.connect.commit()
            question_ids.append(cur.lastrowid)

        for id, q in zip(question_ids, questions):
            for i, ans in enumerate(q.answers):
                if i == q.correct_answer:
                    is_cor = 1
                else:
                    is_cor = 0

                cur.execute("INSERT INTO answers (questions_id, text, is_correct) VALUES(?, ?, ?)",
                            (id, ans, is_cor))
                self.connect.commit()


def main():
    pass


if __name__ == '__main__':
    main()
