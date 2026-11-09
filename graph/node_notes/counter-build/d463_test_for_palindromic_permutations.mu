# REFERENCE: d463 EPI 12.1 Test for palindromic permutations
class Solution
  def can_form_palindrome(s: str) -> bool
    (count odd in counter(s).values()) <= 1
