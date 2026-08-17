def patern(n):
    for i in range(0, n):
        for j in range(0, n - i - 1 + 1):  # Equiv to j <= n-i-1
            print("  ", end="")

        # chr(64) is 'A' - 1 (the character right before 'A')
        ch_code = 64
        breakpoint_val = (2 * i) // 2

        for j in range(0, 2 * i + 1):  # Equiv to j <= 2*i
            if j <= breakpoint_val:
                ch_code += 1
            else:
                ch_code -= 1
            print(chr(ch_code) + " ", end="")

        for j in range(0, n - i - 1 + 1):  # Equiv to j <= n-i-1
            print("  ", end="")

        print()  # Equiv to cout<<endl;


patern(3)
