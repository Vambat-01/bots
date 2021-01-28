from unittest import  TestCase
from algorithms.queue import Queue, ListBasedQueue, LinkedListBasedQueue


class BaseQueueTest(TestCase):
    def check_queue(self, q: Queue):
        self.assertTrue(q.is_empty())
        q.push(1)
        q.push(2)
        q.push(3)
        q.push(4)
        q.push(5)
        actual_pop1 = q.pop()
        actual_pop2 = q.pop()
        self.assertEqual(1, actual_pop1)
        self.assertEqual(2, actual_pop2)
        self.assertFalse(q.is_empty())
        q.pop()
        q.pop()
        q.pop()
        self.assertTrue(q.is_empty())


class ListBasedQueueTest(BaseQueueTest):
    def test_queue(self):
        q = ListBasedQueue()
        self.check_queue(q)


class LinkedListBasedQueueTest(BaseQueueTest):
    def test_queue(self):
        q = LinkedListBasedQueue()
        self.check_queue(q)
