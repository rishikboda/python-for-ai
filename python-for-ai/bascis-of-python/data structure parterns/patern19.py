def patern(n):
    for i in range(1, n):
        for j in range(n - i):
            print(" ", end=" ")
        for j in range(ord("A"), ord("A") + 2 * i - 1):
            print(chr(j), end=" ")
        for j in range(n - 1):
            print(" ", end=" ")
        print(" ")


patern(5)
