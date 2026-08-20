def patern1(n):
    for i in range(n):
        for j in range(n - i):
            print("*", end=" ")
        for j in range(2 * i):
            print(" ", end=" ")
        for j in range(n - i):
            print("*", end=" ")
        print(" ")


def patern2(n):
    for i in range(n + 1):
        for j in range(i):
            print("*", end=" ")
        for j in range(2 * (n - i)):
            print(" ", end=" ")
        for j in range(i):
            print("*", end=" ")
        print(" ")


patern1(5)
patern2(5)
