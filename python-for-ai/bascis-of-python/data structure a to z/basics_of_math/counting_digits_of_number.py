import math


def count_num(n):
    # If the number is 0, print 1 and exit the function early
    if n == 0:
        print(1)

    count = 0
    while n > 0:
        last_digit = n % 10
        count += 1
        n = n // 10
    print(f"digits= {count}")


n = int(input("enter the input of num: "))
count_num(n)

# ___________________(or)_____________
print(f"digits = {len(str(n))}")


# ____________________(or)_____________
count_n = int(math.log10(n) + 1)
print(f"{count_n} digits")
