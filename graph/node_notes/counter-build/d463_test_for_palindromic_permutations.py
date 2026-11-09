# REFERENCE: d463 EPI 12.1 Test for palindromic permutations
class Solution:
    def can_form_palindrome(self, s):
        return sum(n % 2 for n in Counter(s).values()) <= 1
