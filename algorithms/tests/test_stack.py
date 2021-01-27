from unittest import TestCase
from algorithms.stack import StackList, StackLinkedList


class StackListTest(TestCase):
    def test_push(self):
        stack_list = StackList()
        stack_list.push(2)
        stack_list.push(3)
        expected = [2, 3]
        self.assertEqual(expected, stack_list.list)

    def test_pop(self):
        stack_list = StackList()
        stack_list.push(1)
        stack_list.push(3)
        stack_list.push(4)
        actual = stack_list.pop()
        self.assertEqual(4, actual)
        self.assertEqual([1, 3], stack_list.list)

    def test_is_empty_true(self):
        stack_list = StackList()
        self.assertTrue(stack_list.is_empty())

    def test_is_empty_false(self):
        stack_list = StackList()
        stack_list.push(1)
        self.assertFalse(stack_list.is_empty())


class StackLinkedListTest(TestCase):
    def test_push_pop_and_is_empty(self):
        stack_linked_list = StackLinkedList()
        stack_linked_list.push(1)
        stack_linked_list.push(3)
        expected_pop = stack_linked_list.pop()
        self.assertEqual(3, expected_pop)
        self.assertFalse(stack_linked_list.is_empty())
        stack_linked_list.pop()
        self.assertTrue(stack_linked_list.is_empty())

