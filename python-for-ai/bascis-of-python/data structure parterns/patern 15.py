def patern(n):
    number = 1
    for i in range(n):
        for j in range(-1, i):
            print(number, end=" ")
            number += 1
        print(" ")


patern(5)
