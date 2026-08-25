def patern(n):
    for i in range(0, n):
        ch = ord("A")
        # The midpoint index for the current row's characters
        break_point = (2 * i - 1) / 2

        # 1. Print leading double spaces
        for j in range(0, n - i - 1):
            print(" ", end=" ")

        # 2. Print characters with correct increment/decrement logic
        for j in range(0, 2 * i + 1):
            print(chr(ch), end=" ")
            if j < break_point:
                ch += 1
            else:
                ch -= 1

        # 3. Print trailing double spaces
        for j in range(0, n - i - 1):
            print(" ", end=" ")

        # 4. Move to the next row
        print(" ")


patern(4)
