def gcd(a, b):

    while a > 0 and b > 0:
        if a > b:
            a %= b
        else:
            b %= a
        if a == 0:
            print(b)
        if b == 0:
            print(a)


gcd(9, 11)
