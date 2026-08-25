def patern11(n):
    for i in range(0, n + 1):
        start = 1
        if i % 2 == 0:
            start = 1
        else:
            start = 0
        for j in range(0, i):
            start = 1 - start
            print(start, end=" ")
        print(" ")


patern11(5)
