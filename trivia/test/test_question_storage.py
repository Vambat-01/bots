from trivia.question_storage import add_one
import unittest

class AddOneTest(unittest.TestCase):
    def test_add_one_to_three(self):
        x = add_one(3)
        self.assertEqual(4, x)

    def test_add_one_to_four(self):
        x = add_one(4)
        self.assertEqual(5, x)