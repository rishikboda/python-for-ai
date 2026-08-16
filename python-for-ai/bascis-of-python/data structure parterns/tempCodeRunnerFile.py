def patern(n):
    for i in range(1, n):
        for j in range(n - i):
            print(" ")
        for j in range(i, 1):
            print(j)


patern(3)
