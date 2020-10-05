import unittest
from trivia.question_storage import JsonQuestionStorage


class JsonQuestionStorageTest(unittest.TestCase):
    def test_loads_question_correctly(self):
        json_file = "/home/vambat/projects/bots/trivia/test/resources/test_questions.json"
        storage = JsonQuestionStorage(json_file)
        questions = storage.load_questions()
        self.assertEqual(2, len(questions))
        quest = questions[0]
        self.assertEqual("Какое количество цветов у радуги?", quest.text)
        self.assertEqual(2, quest.points)
        self.assertEqual(3, len(quest.answers))
        quest_2 = questions[1]
        self.assertEqual(22, len(quest_2.text))
        self.assertEqual(3, quest_2.points)
        self.assertEqual(2, len(quest_2.answers))

        


