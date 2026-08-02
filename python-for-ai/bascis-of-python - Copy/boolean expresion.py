age =4

has_lisence=True

can_drive = age>=18 and has_lisence

print(can_drive)
age = 21

can_drive = age>=18 or has_lisence
print (can_drive)

drunk =False

can_drive = age>=18 and not drunk

print(can_drive)