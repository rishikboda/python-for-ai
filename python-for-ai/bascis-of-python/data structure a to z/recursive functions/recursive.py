count = 0


def f():
    global count
    if count == 5:
        return
    else:
        print(count)
        count += 1
        f()


f()
