def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid  # Target found
        elif arr[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half

    return -1  # Target not found


sorted_numbers = [1, 8, 3, 2, 4, 5, 6]
target = int(input("enter the element you want to check"))
result = sorted_numbers.sort()
result = binary_search(sorted_numbers, target)

if result != -1:
    print(f"Element found at index: {result}")
else:
    print("Element not found")

    ##note : for the binary search the list must be sort then only it will posiible
