count = 0


def f1():
    global count
    if count == 5:
        return
    else:
        print(count)
        count += 1
        f1()


def f2(i, n):
    if i > n:
        return
    else:
        print("rishi")
        f2(i + 1, n)


def f3(x, y):

    if x > y:
        return
    else:
        print(x)
        f3(x + 1, y)


def f4(a, b):
    if b < 1:
        return
    else:
        print(b)
        f4(a, b - 1)


def f5(n):
    if n == 0:
        return
    else:
        f5(n - 1)
    print(n, end=" ")


def f6(n):
    if n == 0:
        return
    else:
        print(n, end=" ")
        f6(n - 1)


# Output: 5 4 3 2 1

f5(5)  # Output: 1 2 3 4 5
n = int(input())
y = int(input())
b = int(input())

f1()
f2(1, n)
f3(1, y)
f4(1, b)

x = list(map(input().split()))
print(x)
