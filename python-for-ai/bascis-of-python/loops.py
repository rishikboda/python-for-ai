import re

text = "dcjllvaeioAOI"

result = re.sub(r"[aeiouAEIOU]", "", text)

print(result)
for i in range(0, 10):
    print(i)

for i in range(0, 10, 2):
    print(i)

    # here range(0,10,2) means it will print the numbers from 0 to 10
    # and it will print the numbes which are divisible by 2
