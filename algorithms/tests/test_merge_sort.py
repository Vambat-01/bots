from algorithms.merge_sort import merge_sort
from unittest import TestCase
from typing import List


class MergeSortTest(TestCase):
    def check_function(self, nums: List[int], expection: List[int]):
        actual = merge_sort(nums)
        self.assertEqual(actual, expection)

    def test_len_list_1(self):
        nums = [1]
        expection = [1]
        self.check_function(nums, expection)

    def test_merge_sort_1(self):
        nums = [3, 4, 15, 94, 1, 5, 83]
        expection = [1, 3, 4, 5, 15, 83, 94]
        self.check_function(nums, expection)

    def test_merge_sort_2(self):
        nums = [15, 5, 9, 2, 1, 21]
        expection = [1, 2, 5, 9, 15, 21]
        self.check_function(nums, expection)

    def test_merge_sort_3(self):
        nums = [9, 2, 4, 8]
        expection = [2, 4, 8, 9]
        self.check_function(nums, expection)

    def test_merge_sort_4(self):
        nums = [1, 2, 3, 10, 4, 5, 7]
        expection = [1, 2, 3, 4, 5, 7, 10]
        self.check_function(nums, expection)
