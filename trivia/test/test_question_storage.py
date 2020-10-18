import unittest
from trivia.question_storage import JsonQuestionStorage


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

        


