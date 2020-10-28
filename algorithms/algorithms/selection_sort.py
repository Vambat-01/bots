from typing import List


def selection_sort(list_numbs: List[int]):
    for i in range(len(list_numbs)):
        min_ind = i
        for j in range(i + 1, len(list_numbs)):
            if list_numbs[min_ind] > list_numbs[j]:
                min_ind = j
        list_numbs[i], list_numbs[min_ind] = list_numbs[min_ind], list_numbs[i]








