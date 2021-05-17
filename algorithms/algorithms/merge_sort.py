from typing import List


def merge(a: List[int], b: List[int]) -> List[int]:
    ind_a = 0
    ind_b = 0
    c = []
    while len(a) != ind_a or len(b) != ind_b:
        if len(a) != ind_a and len(b) != ind_b:
            if a[ind_a] < b[ind_b]:
                c.append(a[ind_a])
                ind_a += 1
            else:
                c.append(b[ind_b])
                ind_b += 1
        elif len(a) != ind_a:
            c.append(a[ind_a])
            ind_a += 1
        else:
            c.append(b[ind_b])
            ind_b += 1
    return c


def merge_sort(nums: List[int]) -> List[int]:
    if len(nums) < 2:
        return nums
    middle = len(nums) // 2
    left = merge_sort(nums[:middle])
    right = merge_sort(nums[middle:])
    return merge(left, right)


nums = [3, 4, 15, 94, 1, 5, 83]
print(merge_sort(nums))
