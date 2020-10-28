from unittest import TestCase
from algorithms.contains import contains_4


class ContainsTest(TestCase):
    def test_contains_name(self):
        where = "My name is Bob"
        what = "Bob"
        check = contains_4(where, what)
        self.assertEqual(True, check)

    def test_contains_date(self):
        where = "I was born in 1988"
        what = "1988"
        check = contains_4(where, what)
        self.assertEqual(True, check)

    def test_contains_false(self):
        where = "I was born in 1988"
        what = "28"
        check = contains_4(where, what)
        self.assertEqual(False, check)

    def test_contains_false_second(self):
        where = "Hello world"
        what = "he"
        check = contains_4(where, what)
        self.assertEqual(False, check)

    def test_contains_aaaa(self):
        where = "aaabaaa"
        what = "aaaa"
        check = contains_4(where, what)
        self.assertEqual(False, check)

    def test_contains_abc(self):
        where = "abcd"
        what = "abc"
        check = contains_4(where, what)
        self.assertEqual(True, check)
