def pattern(n):
    for i in range(n):
        # ord('A') is 65. The inner loop generates integer ASCII codes.
        for j in range(ord("A"), ord("A") + i + 1):
            # chr(j) converts the ASCII integer back to a character
            print(chr(j), end=" ")
        print()  # Moves to the next line


pattern(5)
