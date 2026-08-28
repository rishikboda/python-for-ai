def f1(i, name):
    # 1. Check if we have reached the middle of the word
    if i >= len(name) // 2:
        return True

    # 2. Compare the front letter with the matching back letter
    if name[i] != name[len(name) - i - 1]:
        # If they do not match, it is not a palindrome
        return False

    # 3. Move to the next set of letters
    return f1(i + 1, name)


name = "madam"
print(f1(0, name))
