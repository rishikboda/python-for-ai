def patern(n):
    for i in range(2 * n - 1):
        for j in range(2 * n - 1):
            top = i
            down = j
            right = (2 * n - 2) - i
            left = (2 * n - 2) - j
            print(n - min(min(top, down), min(left, right)), end=" ")
        print(" ")


patern(5)
