n = int(input("enter the nummber of elements"))
my_lists = list(map(int, input("enter the elements of the list").split()))
print(my_lists)
# in this way we can  take the input from the user for the datastructure list
# to find the specific element weither it is lagest or smallest we sould make in the accending order
# to make accending order we use sort
my_lists.sort()
print(my_lists)
# here i want to know the largest element of my list
print(my_lists[-1])
# so by using index we can find the elements
