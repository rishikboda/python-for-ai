#Combining strings

first_name= "rishi"
second_name ="k"
full_name = first_name + second_name
print(full_name)
#if we want to add the space betweeen the two name just write first_name +" "+second_name


#length of the strings 
name ="rishik"
print(len(name))


#converting strings
age = 10
print (f"rishik is {age} old")
#here i used f string to print we i did not write f then it will give like this rishik is {age} old
#or we can write the same like this
age =19
message ="rishik is a good boy he is " + str(age) + " old"
print (message)
# here we should use the + operator to chage the integer data type 19 to string 


# Wrong
#result = "Age: " + 25  # TypeError!

# Right - convert number first
result = "Age: " + str(25)