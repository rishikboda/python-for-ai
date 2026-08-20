def patern1(n):
    for i in range(1, n + 1):
        # 1. Left side: print numbers ascending from 1 to i
        for j in range(1, i + 1):
            print(j, end=" ")

        # 2. Middle: print spaces that shrink as i grows
        for j in range(2 * (n - i)):
            print(" ", end=" ")

        # 3. Right side: print numbers descending from i to 1
        for j in range(i, 0, -1):
            print(j, end=" ")

        print()


patern1(3)
