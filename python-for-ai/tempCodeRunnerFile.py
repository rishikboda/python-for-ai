my_list = [10, 3, 2, 1, 5]
swaped = True
while swaped:
    swaped = False

    for i in range(len(my_list) - 1):
        if my_list[i] > my_list[i + 1]:
            swaped = True
            my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]
print(my_list)