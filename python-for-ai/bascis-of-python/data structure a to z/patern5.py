def patern(n):
    for i in range(0, n):
        for j in range(n - i):
            print("*", end=" ")
        print(" ")


patern(5)
