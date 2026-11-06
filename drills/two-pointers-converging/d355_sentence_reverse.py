"""
Given a list arr of characters, return arr with the order of its words
reversed, changed in place. A word is a run of characters that are not
' '. In the result, a ' ' at index i of arr is at index
len(arr) - 1 - i, and the words fill the other positions in reverse
order, each word with its characters in their original order.

Example 1:

Input: arr = ['a', ' ', ' ', 'b']
Output: ['b', ' ', ' ', 'a']

Example 2:

Input: arr = ['p', 'e', 'r', 'f', 'e', 'c', 't', ' ', 'm', 'a', 'k', 'e', 's', ' ', 'p', 'r', 'a', 'c', 't', 'i', 'c', 'e']
Output: ['p', 'r', 'a', 'c', 't', 'i', 'c', 'e', ' ', 'm', 'a', 'k', 'e', 's', ' ', 'p', 'e', 'r', 'f', 'e', 'c', 't']

Example 3:

Input: arr = [' ', 'a', 'b']
Output: ['a', 'b', ' ']
Explanation: the ' ' at index 0 is at index 2 in the result.

Constraints:

    0 <= len(arr) <= 100
    arr[i] is a lowercase English letter or ' '.

    REQUIRED: O(n) time, O(1) extra space, in place. NO new list, NO
    split, NO join, NO slicing.
"""


class Solution:
    def reverse_words(self, arr: list[str]) -> list[str]:
        pass


sol = Solution()

print(sol.reverse_words(['a', ' ', ' ', 'b']))  # ['b', ' ', ' ', 'a']

# assert sol.reverse_words(['a', ' ', ' ', 'b']) == ['b', ' ', ' ', 'a']
# assert sol.reverse_words(['p', 'e', 'r', 'f', 'e', 'c', 't', ' ', 'm', 'a', 'k', 'e', 's', ' ', 'p', 'r', 'a', 'c', 't', 'i', 'c', 'e']) == ['p', 'r', 'a', 'c', 't', 'i', 'c', 'e', ' ', 'm', 'a', 'k', 'e', 's', ' ', 'p', 'e', 'r', 'f', 'e', 'c', 't']
# assert sol.reverse_words([' ', 'a', 'b']) == ['a', 'b', ' ']
# assert sol.reverse_words([' ', ' ']) == [' ', ' ']
# assert sol.reverse_words(['h', 'e', 'l', 'l', 'o']) == ['h', 'e', 'l', 'l', 'o']
# assert sol.reverse_words(['y', 'o', 'u', ' ', 'w', 'i', 't', 'h', ' ', 'b', 'e', ' ', 'f', 'o', 'r', 'c', 'e', ' ', 't', 'h', 'e', ' ', 'm', 'a', 'y']) == ['m', 'a', 'y', ' ', 't', 'h', 'e', ' ', 'f', 'o', 'r', 'c', 'e', ' ', 'b', 'e', ' ', 'w', 'i', 't', 'h', ' ', 'y', 'o', 'u']
# assert sol.reverse_words(['g', 'r', 'e', 'a', 't', 'e', 's', 't', ' ', 'n', 'a', 'm', 'e', ' ', 'f', 'i', 'r', 's', 't', ' ', 'e', 'v', 'e', 'r', ' ', 'n', 'a', 'm', 'e', ' ', 'l', 'a', 's', 't']) == ['l', 'a', 's', 't', ' ', 'n', 'a', 'm', 'e', ' ', 'e', 'v', 'e', 'r', ' ', 'f', 'i', 'r', 's', 't', ' ', 'n', 'a', 'm', 'e', ' ', 'g', 'r', 'e', 'a', 't', 'e', 's', 't']
# assert sol.reverse_words([]) == []
# assert sol.reverse_words(['a']) == ['a']
# assert sol.reverse_words([' ']) == [' ']
# assert sol.reverse_words(['a', ' ']) == [' ', 'a']
# assert sol.reverse_words(['a', 'b', ' ', 'c']) == ['c', ' ', 'a', 'b']
# assert sol.reverse_words(['a', ' '] * 50) == [' ', 'a'] * 50
# assert sol.reverse_words(['a'] * 100) == ['a'] * 100
# assert sol.reverse_words(['a', 'b', ' '] * 33) == [' ', 'a', 'b'] * 33
# arr = ['a', ' ', 'b']
# assert sol.reverse_words(arr) is arr
