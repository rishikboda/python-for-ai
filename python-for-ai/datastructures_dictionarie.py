#Dictionaries store data in key-value pairs. 
# Think of them like a real dictionary where you look up a word 
# (key) to find its definition (value).
person = {
    "name" :"rishik",
    "age" : 19,
    "city" : "rajkot"
}
print(person)

#add or update
person["email"]="rishikboda@gmail.com"
print(person)

# Update multiple values
person.update({"age": 31, "job": "Engineer"})
print(person)


# Get all keys, values, or items
print(person.keys())    # dict_keys(['name', 'age', 'city'])
print(person.values())  # dict_values(['Alice', 30, 'New York'])
print(person.items())   # dict_items([('name', 'Alice'), ...])

# Check if key exists
if "name" in person:
    print("Name found!")

#nested dictionarys

students = {
    "alice": {"age": 20, "grade": "A"},
    "bob": {"age": 21, "grade": "B"},
    "charlie": {"age": 19, "grade": "A"}
}

# Access nested data
print(students["alice"]["grade"])  # "A"


# Different ways to create
scores = dict(math=95, english=87, science=92)
