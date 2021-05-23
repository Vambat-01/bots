from algorithms.merge_sort import merge_sort
from unittest import TestCase
from typing import List


class MergeSortTest(TestCase):
    def check(self, nums: List[int], expected: List[int]):
        actual = merge_sort(nums)
        self.assertEqual(actual, expected)

    def test_len_list_1(self):
        nums = [1]
        expected = [1]
        self.check(nums, expected)

    def test_merge_sort_1(self):
        nums = [3, 4, 15, 94, 1, 5, 83]
        expected = [1, 3, 4, 5, 15, 83, 94]
        self.check(nums, expected)

    def test_merge_sort_2(self):
        nums = [15, 5, 9, 2, 1, 21]
        expected = [1, 2, 5, 9, 15, 21]
        self.check(nums, expected)

    def test_merge_sort_3(self):
        nums = [9, 2, 4, 8]
        expected = [2, 4, 8, 9]
        self.check(nums, expected)

    def test_merge_sort_4(self):
        nums = [1, 2, 3, 10, 4, 5, 7]
        expected = [1, 2, 3, 4, 5, 7, 10]
        self.check(nums, expected)
