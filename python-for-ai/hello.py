print("hello world!")
# to make some change in your file and want to upload it the changed file in github
# follow these commands
# git add .
# git status
# git commit -m "made some changes"
# git push

# and now save the file in vscode and do the changes in the git hub
my_list = [10, 3, 2, 1, 5]
swaped = True
while swaped:
    swaped = False

    for i in range(len(my_list) - 1):
        if my_list[i] > my_list[i + 1]:
            swaped = True
            my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]
print(my_list)
