def patern7(n):
    for i in range(0, n):
        for j in range(0, n - i - 1):
            print(" ", end=" ")
        for j in range(0, 2 * i + 1):
            print("*", end=" ")
        for j in range(0, n - i - 1):
            print(" ", end=" ")
        print(" ")


patern7(5)
