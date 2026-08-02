name = "rishi"
age =10
age=age/2
print(age)
#here it will give the value in the float data type where as in c++ or c it will give in int
# so if we want in the int data type we should write the code like
age2 =10
age2 =age2//2
print(age2)

# Powers
squared = 5 ** 2   # 25
cubed = 2 ** 3     # 8
#if we want to check the data type og the age variable 
print(type(age)) #<class 'float'>


# Wrong
million = 1,000,000  # Creates a tuple, not a number!

# Right
million = 1000000    # Hard to read
million = 1_000_000  # Python style
 