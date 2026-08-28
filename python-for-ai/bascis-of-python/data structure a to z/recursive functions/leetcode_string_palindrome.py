class Solution(object):
    def isPalindrome(self, s, i=0):
        # Only clean the string once, on the very first call
        if i == 0:
            try:
                s = s.lower()
                s = s.lower()
                s = s.replace(" ", "")
                s = s.replace(",", "")
                s = s.replace(":", "")
                s = s.replace(".", "")
                s = s.replace("'", "")
                s = s.replace("!", "")
                s = s.replace("?", "")
                s = s.replace(";", "")

            except:
                s = s.lower()
                s = "".join(filter(str.isalnum, s))

        # Base case: reached the middle, no mismatches found
        if i >= len(s) // 2:
            return True

        # Compare front character with matching back character
        if s[i] != s[len(s) - i - 1]:
            return False

        # Move inward and check the next pair
        return self.isPalindrome(s, i + 1)


# Manual testing
sol = Solution()
print(sol.isPalindrome("Race car"))  # True
print(sol.isPalindrome("A man, a plan, a canal: Panama"))  # True
print(sol.isPalindrome("race a car"))  # False
print(sol.isPalindrome(" "))  # True
print(sol.isPalindrome(":aa/"))  # True


# note:it will not work for the all test cases in leet code so
# if you want to run all the test cases use only the except condition
