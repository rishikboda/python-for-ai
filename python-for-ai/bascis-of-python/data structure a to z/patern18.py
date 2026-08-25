def pattern(n):
    for i in range(n):
        # Calculate the ASCII character string (e.g., 'A', 'B', 'C'...)
        char = chr(ord("A") + i)
        # Loop i + 1 times to print that character across the columns
        for j in range(i + 1):
            print(char, end=" ")
        print(" ")  # Move to the next row


pattern(5)
