import json
from typing import List, Dict
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from collections import defaultdict
from enum import Enum
from pathlib import Path
import sqlite3
from dataclasses_json import dataclass_json


class CreateDatabaseException(Exception):
    """
    Ошибка создания SQLite базы данных
    """
    pass


@dataclass_json
@dataclass(frozen=True)
class Question:
    """
    Представляет собой trivia bot  вопрос
    :param text: Текст вопроса, который мы показываем пользователю
    :param answers: Варианты ответов на вопрос, включая правильный
    :param points: Количество очков за правильный ответ
    :param difficulty: Сложность вопроса
    :param correct_answer: Правильный ответ. Индекс правильного ответа в списке `answers`
    """

    class Difficulty(Enum):
        EASY = 0
        MEDIUM = 1
        HARD = 2

    text: str
    answers: List[str]
    points: int
    difficulty: Difficulty
    correct_answer: int

    def normalize(self) -> "Question":
        """
            Создает эквивалентный вопрос, но с отсортированными по алфавиту ответами
        :return: отсортированный Question
        """
        check_ans = self.answers[self.correct_answer]
        norm_answers = sorted(self.answers)
        norm_correct_answer = norm_answers.index(check_ans)

        return Question(self.text, norm_answers, self.points, self.difficulty, norm_correct_answer)


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
            Cчитывает список вопросов из json файла
        :return: список вопросов
        """
        with open(self.file_path) as json_file:
            data = json.load(json_file)
            q_str = JSONEncoder().encode(data)
            q_restored_json = JSONDecoder().decode(q_str)
            q_restored = Question.schema().load(q_restored_json, many=True)     # type: ignore
            return q_restored


class SqliteQuestionStorage(QuestionStorage):
    """
        Класс для чтения вопросов из SQLite базы данных
    """

    @dataclass(frozen=True)
    class Record:
        """
            Класс для удобного хранения вопроса из SQLite базы данных
        """
        question_text: str
        points: int
        difficulty: int
        question_id: int
        answer_text: str
        is_correct: bool

    @staticmethod
    def create_in_memory() -> "SqliteQuestionStorage":
        """
        Создает SQLiteQuestionStorage с базой в памяти и все необходимые таблицы. Таблицы будут пустыми
        но они не заполнены
        :return: созданный `SqliteQuestionStorage`
        """
        connection = sqlite3.connect(":memory:")
        return SqliteQuestionStorage._create(connection)

    @staticmethod
    def create_in_file(file_path: Path) -> "SqliteQuestionStorage":
        """
        Создает SQLite базу данных и все необходимые таблицы. Таблицы будут пустыми.
        :param file_path: путь где будет создана база. Наличие файла по этому пути приведет к ошибке.
        """
        if file_path.exists():
            raise CreateDatabaseException("SQLite database already exists")

        connection = sqlite3.connect(file_path)
        return SqliteQuestionStorage._create(connection)

    @staticmethod
    def _create(connection: sqlite3.Connection) -> "SqliteQuestionStorage":
        """
        Сощдаст все необходимые таблицы в SQLite базе данных. Таблицы будут пустыми
        :param connection: подключение к базе данных
        """
        cur = connection.cursor()
        cur.executescript("""
                                                   CREATE TABLE questions (
                                                   id INTEGER PRIMARY KEY,
                                                   text TEXT,
                                                   points INTEGER NOT NULL,
                                                   difficulty INTEGER NOT NULL
                                                   );

                                                   CREATE TABLE answers (
                                                   id INTEGER PRIMARY KEY,
                                                   questions_id INTEGER NOT NULL,
                                                   text TEXT NOT NULL,
                                                   is_correct INTEGER NOT NULL,
                                                   FOREIGN KEY(questions_id) REFERENCES questions (id))
                                                   """)
        return SqliteQuestionStorage(connection)

    @staticmethod
    def save_to_file(questions: str, file_path: Path):
        """
        Записывает переданные вопросы в файл в json формате
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(questions)

    def __init__(self, connection: sqlite3.Connection):
        """
        :param connection: подключение к базе данных
        """
        self.connection = connection

    def load_questions(self) -> List[Question]:
        """
            Считывает список вопросов из базы данных
        :return: список вопросов
        """
        cur = self.connection.cursor()
        items = cur.execute("""
                            SELECT t1.text, t1.points, t1.difficulty, t2.questions_id, t2.text, t2.is_correct
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
            difficulty = Question.Difficulty(records[0].difficulty)

            answers = [r.answer_text for r in records]

            correect_answer_index = [r.is_correct for r in records].index(True)

            questions.append(Question(text, answers, points, difficulty, correect_answer_index))
        return questions

    def add_questions(self, questions: List[Question]):
        """
            Добавляет вопросы в базу данных
        :param questions: Список вопросов
        """
        cur = self.connection.cursor()
        question_ids = []
        for quest in questions:
            difficulty = quest.difficulty.value
            cur.execute("INSERT INTO questions(text, points, difficulty) VALUES(?, ?, ?)",
                        (quest.text, quest.points, difficulty))
            question_ids.append(cur.lastrowid)
        self.connection.commit()

        for id, q in zip(question_ids, questions):
            for i, ans in enumerate(q.answers):
                if i == q.correct_answer:
                    is_cor = 1
                else:
                    is_cor = 0

                cur.execute("INSERT INTO answers (questions_id, text, is_correct) VALUES(?, ?, ?)",
                            (id, ans, is_cor))
        self.connection.commit()


class JSONEncoder(json.JSONEncoder):
    """
    Расширяет класс JSONEncoder, чтобы он мог кодировать Enum класс Difficulty
    """
    def default(self, obj):
        if isinstance(obj, Question.Difficulty):
            return {
                "__difficulty": obj.value
            }
        return json.JSONEncoder.default(self, obj)


class JSONDecoder(json.JSONDecoder):
    """
    Расширяет класс JSONDecoder, чтобы он мог декодировать Enum класс Difficulty
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            if "__difficulty" in obj:
                return Question.Difficulty(obj.get("__difficulty"))
        return obj


def main():
    pass


if __name__ == '__main__':
    main()
