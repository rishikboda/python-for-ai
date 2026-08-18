def patern(n):
    for i in range(0, n):
        for j in range(ord("E") - i, ord("E") + 1):
            print(chr(j), end=" ")
        print(" ")


patern(5)
