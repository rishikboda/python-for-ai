def f1(i, sum):
    if i < 1:
        print(sum)
        return

    else:
        f1(i - 1, sum + i)


f1(5, 0)
