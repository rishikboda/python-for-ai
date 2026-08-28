class solution:
    def palindrome(self, i, name):
        name.lower()
        name.remove(" ")
        if i >= name.len() / 2:
            return True
        if name[i] != name[name.len() - i - 1]:
            return False
        return self.palindrome(i + 1, name)


s = solution()
x = s.palindrome(0, "name is rishDHDIL BDBjv ")

print(x)
