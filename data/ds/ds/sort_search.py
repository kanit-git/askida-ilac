def mergesort(arr, key_index):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergesort(arr[:mid], key_index)
    right = mergesort(arr[mid:], key_index)

    return merge(left, right, key_index)


def merge(left, right, key_index):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][key_index] <= right[j][key_index]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def binary_search(sorted_arr, tc, tc_index=1):
    low = 0
    high = len(sorted_arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_arr[mid][tc_index] == tc:
            return sorted_arr[mid]
        elif sorted_arr[mid][tc_index] < tc:
            low = mid + 1
        else:
            high = mid - 1

    return None
