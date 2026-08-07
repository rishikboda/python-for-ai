def linear_search(arr, taget):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


numbers = [1, 2, 3, 4, 5]
target = 2
result = linear_search(numbers, target)
if result != -1:
    print(f"element found at the index : {result}")
else:
    print("element not found")
