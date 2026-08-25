def patern2(n):
    for i in range(n):
        for j in range(-1, i):
            print("*", end=" ")
        print(" ")


t = int(input(" enter the parterns you want"))
for i in range(t):
    n = int(input("enter the partern size n*n"))
    patern2(n)
