class Solution(object):
    def isPalindrome(self, x):
        original_value = x

        reversed_number = int(str(abs(x))[::-1])
        if x < 0:
            return False
        if original_value == reversed_number:
            return True
        else:
            return False


solution = Solution()
result = solution.isPalindrome(151)
print(result)
