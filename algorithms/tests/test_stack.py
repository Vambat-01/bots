from unittest import TestCase
from algorithms.stack import ListBasedStack, LinkedListBasedStack, Stack


class BaseStackTest(TestCase):
    def check_stack(self, s: Stack) -> None:
        self.assertTrue(s.is_empty())
        s.push(1)
        s.push(3)
        actual_pop = s.pop()
        self.assertEqual(3, actual_pop)
        self.assertFalse(s.is_empty())
        s.pop()
        self.assertTrue(s.is_empty())


class ListBasedStackTest(BaseStackTest):
    def test_stack(self):
        s = ListBasedStack()
        self.check_stack(s)


class LinkedListBasedStackTest(BaseStackTest):
    def test_stack(self):
        s = LinkedListBasedStack()
        self.check_stack(s)
