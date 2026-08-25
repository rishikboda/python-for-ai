def pattern(n):
    for i in range(1, n + 1):
        for j in range(n - i):
            print(" ", end="")
        for j in range(i, 0, -1):
            # here range(i,0,-1) means start stop and step
            # means the loop will start from i
            # it will end at 0
            # -1 indicates the loop run in backwards
            # for example in c++ we use i-- for decrement
            # in python we use just -1
            print(j, end="")
        print()


pattern(3)
