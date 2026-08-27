def amsterdong(n):
    sum = 0
    original = n

    while n != 0:
        last_digit = n % 10
        sum = sum + (last_digit * last_digit * last_digit)
        n = n // 10
    if sum == original:
        print(f"{sum} is an amsterdong number")
    else:
        print(f"{sum} is not an amsterdong number")


amsterdong(371)
