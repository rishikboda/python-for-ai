def patern(n):
    for i in range(0, n):
        for j in range(i):
            print("*", end=" ")
        print(" ")


def patern1(n):
    for i in range(0, n):
        for j in range(n - i):
            print("*", end=" ")
        print(" ")


n = int(input("enter the number of rows"))
patern(n)
patern1(n)
