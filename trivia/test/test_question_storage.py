import unittest
from trivia.question_storage import JsonQuestionStorage, SqliteQuestionStorage, Question
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
    def test_add_load(self):

        test_questions = [
                            Question("15+5", ["30", "20", "15"], 2, Question.Difficulty.MEDIUM, 1),
                            Question("25+5", ["35", "25", "30"], 3, Question.Difficulty.HARD, 2)
                         ]
        storage = SqliteQuestionStorage.create_in_memory()
        storage.add_questions(test_questions)
        questions = storage.load_questions()
        norm_questions = get_sorted_questions(questions)

        self.assertEqual(
            [
                Question("15+5", ["15", "20", "30"], 2, Question.Difficulty.MEDIUM, 1),
                Question("25+5", ["25", "30", "35"], 3, Question.Difficulty.HARD, 1)
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
