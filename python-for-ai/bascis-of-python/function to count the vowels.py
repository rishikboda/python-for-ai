name = input("enter the value of the name")
def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count


# Example usage
print(count_vowels(name))   # Output: 3
print(count_vowels("PYTHON"))        # Output: 1
print(count_vowels("aeiou"))         # Output: 5
