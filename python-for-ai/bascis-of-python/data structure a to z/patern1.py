def patern(n):
    for i in range(0, n):
        for j in range(0, n):
            print("*", end=" ")
        print(" ")


t = int(input(" enter the parterns you want"))
for i in range(0, t):
    n = int(input("enter the partern size n*n"))
    patern(n)
