from unittest import TestCase
from algorithms.insertion_sort import insertion_sort
from typing import List


class InsertionSortTest(TestCase):
    def check_function(self, data: List[int]):
        data_2 = data.copy()
        insertion_sort(data)
        data_2.sort()
        self.assertEqual(data, data_2)

    def test_positive_numbers_2(self):
        data = [4, 1, 2, 5, 7]
        self.check_function(data)

    def test_positive_numbers(self):
        data = [4, 2, 5]
        self.check_function(data)

    def test_negative_numbers(self):
        data = [-4, -1, -2, -5, -7]
        self.check_function(data)

    def test_mixed_numbers(self):
        data = [-4, 1, -2, 5, -7]
        self.check_function(data)

    def test_empty_list(self):
        data = []
        self.check_function(data)

    def test_duplicated_numbers(self):
        data = [-1, -1, -2, 0, 0]
        self.check_function(data)

    def test_same_numbers(self):
        data = [1, 1, 1, 1, 1]
        self.check_function(data)

    def test_one_elem(self):
        data = [1]
        self.check_function(data)

