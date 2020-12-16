from typing import List, Callable


# def selection_sort(list_numbs: List[int]):
#     for i in range(len(list_numbs)):
#         min_ind = i
#         for j in range(i + 1, len(list_numbs)):
#             if list_numbs[min_ind] > list_numbs[j]:
#                 min_ind = j
#         list_numbs[i], list_numbs[min_ind] = list_numbs[min_ind], list_numbs[i]


def selection_sort_key(data: List[int], key: Callable[[int], int]):
    for i in range(len(data)):
        min_ind = i

        for j in range(i + 1, len(data)):
            if key(data[min_ind]) > key(data[j]):
                min_ind = j
        data[i], data[min_ind] = data[min_ind], data[i]


items = [5, 2, 6, 1]
selection_sort_key(items, lambda x: -x)
print(items)





