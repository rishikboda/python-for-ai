def patern7(n):
    for i in range(0, n):
        for j in range(0, n - i - 1):
            print(" ", end=" ")
        for j in range(0, 2 * i + 1):
            print("*", end=" ")
        for j in range(0, n - i - 1):
            print(" ", end=" ")
        print(" ")


def patern(n):
    for i in range(0, n):
        for j in range(0, i):
            print(" ", end=" ")
        for j in range(0, 2 * n - (2 * i + 1)):
            print("*", end=" ")
        for j in range(0, i):
            print(" ", end=" ")
        print(" ")


n = int(input("enter the number of rows"))
patern7(n)
patern(n)
