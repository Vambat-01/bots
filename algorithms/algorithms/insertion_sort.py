from typing import List, Callable


# def insertion_sort(data: List[int]):
#     for i in range(1, len(data)):
#         j = i
#         while j > 0 and data[j - 1] > data[j]:
#           data[j - 1], data[j] = data[j], data[j - 1]
#           j -= 1
#     return data
#
#
# data = [4, 3, 2, 1]
# print(insertion_sort(data))
#
# def insertion_sort(list_numbs: List[int]):
#     for i in range(1, len(list_numbs)):
#         num_insert = list_numbs[i]
#         j = i - 1
#         while j >= 0 and list_numbs[j] > num_insert:
#             list_numbs[j + 1] = list_numbs[j]
#             j -= 1
#         list_numbs[j + 1] = num_insert
#
#


def insertion_sort(data: List[int], key: Callable[[int], int]):
    for i in range(1, len(data)):
        j = i
        while j > 0 and key(data[j - 1]) > key(data[j]):
          data[j - 1], data[j] = data[j], data[j - 1]
          j -= 1


items = [5, 2, 6, 1]
insertion_sort(items, lambda x: x)
print(items)


# Лучший - O(n)
# Худший - O(n^2)