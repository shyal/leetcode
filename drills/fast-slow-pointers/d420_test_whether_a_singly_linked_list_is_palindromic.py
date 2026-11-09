"""
EPI 7.11 Test whether a singly linked list is palindromic

Given the head L of a linked list, return True when the sequence of its
values reads the same forwards and backwards, and False otherwise. An
empty list is a palindrome. You are allowed to relink the nodes of L.

Example 1:

Input: L = [1, 2, 3, 2, 1]
Output: True

Example 2:

Input: L = [1, 2, 2, 3]
Output: False

Example 3:

Input: L = [4, 4]
Output: True

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= Node.val <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO list of values, NO list
    of nodes, NO string of the values, NO recursion.
"""


class Solution:
    def is_linked_list_a_palindrome(self, L: ListNode | None) -> bool:
        pass


sol = Solution()

print(sol.is_linked_list_a_palindrome(build_linked_list([1, 2, 3, 2, 1])))  # True


def pal(vals):
    return sol.is_linked_list_a_palindrome(build_linked_list(vals))


# assert pal([1, 2, 3, 2, 1]) is True
# assert pal([1, 2, 2, 3]) is False
# assert pal([4, 4]) is True
# assert pal([]) is True
# assert pal([7]) is True
# assert pal([1, 2]) is False
# assert pal([1, 2, 1]) is True
# assert pal([1, 2, 2, 1]) is True
# assert pal([1, 2, 3, 1]) is False
# assert pal([2, 1, 1]) is False
# assert pal([1, 1, 2]) is False
# assert pal([-5, 0, 0, -5]) is True
# assert pal(list(range(5 * 10 ** 4)) + list(range(5 * 10 ** 4 - 1, -1, -1))) is True
# assert pal(list(range(5 * 10 ** 4)) + list(range(5 * 10 ** 4 - 2, -1, -1))) is True
# assert pal(list(range(5 * 10 ** 4)) + list(range(5 * 10 ** 4 - 1, 0, -1)) + [7]) is False
# assert pal([3] * (10 ** 5 - 1) + [4]) is False
