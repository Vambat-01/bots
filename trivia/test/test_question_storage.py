import unittest
from trivia.question_storage import JsonQuestionStorage, SqliteQuestionStorage, Question
import sqlite3
from typing import List


class JsonQuestionStorageTest(unittest.TestCase):
    def test_loads_question_correctly(self):
        json_file = "resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        self.assertEqual(3, len(questions))
        quest = questions[0]
        self.assertEqual("7+3", quest.text)
        self.assertEqual(1, quest.points)
        self.assertEqual(2, len(quest.answers))
        quest_2 = questions[1]
        self.assertEqual(4, len(quest_2.text))
        self.assertEqual(2, quest_2.points)
        self.assertEqual(2, len(quest_2.answers))


class SqliteQuestiosStorageTest(unittest.TestCase):
    def test_load_questions(self):
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
                                                  FOREIGN KEY(questions_id) REFERENCES questions (id)
                                                 );
                            INSERT INTO questions (id, text, points) VALUES ("1", "7+3", "1");
                            INSERT INTO questions (id, text, points) VALUES ("2", "17+3", "3");
                            INSERT INTO answers (id, questions_id, text, is_correct) 
                            VALUES ("1", "1", "10", "1");
                            INSERT INTO answers (id, questions_id, text, is_correct) 
                            VALUES ("2", "1", "15", "0");
                            INSERT INTO answers (id, questions_id, text, is_correct) 
                            VALUES ("3", "2", "25", "0");
                            INSERT INTO answers (id, questions_id, text, is_correct) 
                            VALUES ("4", "2", "20", "1");                       
                        """)

        storage = SqliteQuestionStorage(connection)
        questions = storage.load_questions()
        norm_questions = get_sorted_questions(questions)

        self.assertEqual(
            [
                Question("17+3", ["20", "25"], 3, 0),
                Question("7+3", ["10", "15"], 1, 0)
            ],
            norm_questions
        )

    def test_add_questions(self):

        test_questions = [
                            Question("15+5", ["30", "20", "15"], 2, 1),
                            Question("25+5", ["35", "25", "30"], 3, 2)
                         ]
        storage = SqliteQuestionStorage.create_in_memory()
        storage.add_questions(test_questions)
        questions = storage.load_questions()
        norm_questions = get_sorted_questions(questions)

        self.assertEqual(
            [
                Question("15+5", ["15", "20", "30"], 2, 1),
                Question("25+5", ["25", "30", "35"], 3, 1)
            ],
            norm_questions
        )


def get_sorted_questions(questions: List[Question]) -> List[Question]:
    questions.sort(key=lambda p: p.text)
    sort_questions = []

    for q in questions:
        sort_quest = q.normalize()
        sort_questions.append(sort_quest)

    return sort_questions
