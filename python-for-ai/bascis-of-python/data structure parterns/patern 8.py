def patern(n):
    for i in range(0, n):
        for j in range(0, n + i - 3):
            print(" ", end=" ")
        for j in range(0, (2 * n - 1) - 2 * i):
            print("*", end=" ")
        for j in range(0, n + i - 3):
            print(" ", end=" ")
        print(" ")


patern(5)
