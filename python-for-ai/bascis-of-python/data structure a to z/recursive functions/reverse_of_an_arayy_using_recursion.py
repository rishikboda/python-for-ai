def swap2(x, arr, n):
    if x >= n // 2:
        return
    else:
        temp = arr[x]
        arr[x] = arr[n - 1 - x]
        arr[n - 1 - x] = temp
        swap2(x + 1, arr, n)


n = 5
arr = [1, 2, 3, 4, 5]
swap2(0, arr, n)
print(arr)
# simple by using python in build function we can reverse
# an array but to uderstand the concept of recursion i use this method
arr.reverse()
print(arr)
# if you observe first the function swap revrese the array or list
# into 54321 and then inbuild function reverse
# again reverse and kept the array in normal 12345
