def patern(n):
    for i in range(n):
        for j in range(-1, i):
            print(i + 1, end=" ")
        print(" ")


patern(5)
