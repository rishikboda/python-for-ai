num = 5
factorial = 1
for i in range(1,num+1):
    factorial=factorial*i

    print(factorial)

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result = result * i
    return result
n = int(input("enter the number"))
print(factorial(n))   # Output: 120