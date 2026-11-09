"""
EPI 7.13 Add list-based integers

Given the heads L1 and L2 of two linked lists, each of which holds the
decimal digits of a nonnegative integer with the least significant
digit first, return the head of a new list that holds the digits of
their sum in the same form.

Example 1:

Input: L1 = [3, 1, 4], L2 = [7, 0, 9]
Output: [0, 2, 3, 1]
Explanation: 413 + 907 = 1320.

Example 2:

Input: L1 = [9, 9], L2 = [1]
Output: [0, 0, 1]
Explanation: 99 + 1 = 100.

Example 3:

Input: L1 = [0], L2 = [0]
Output: [0]

Constraints:

    1 <= number of nodes in L1, L2 <= 10^4
    0 <= Node.val <= 9
    Neither list has a leading zero, except the list [0].

    REQUIRED: O(n + m) time. NO conversion of a list to an int or a
    str, NO list of digits.
"""


class Solution:
    def add_two_numbers(self, L1: ListNode, L2: ListNode) -> ListNode:
        pass


sol = Solution()

print(get_list_values(sol.add_two_numbers(build_linked_list([3, 1, 4]), build_linked_list([7, 0, 9]))))  # [0, 2, 3, 1]


def add(a, b):
    return get_list_values(sol.add_two_numbers(build_linked_list(a), build_linked_list(b)))


# assert add([3, 1, 4], [7, 0, 9]) == [0, 2, 3, 1]
# assert add([9, 9], [1]) == [0, 0, 1]
# assert add([1], [9, 9]) == [0, 0, 1]
# assert add([0], [0]) == [0]
# assert add([0], [5, 4]) == [5, 4]
# assert add([5], [5]) == [0, 1]
# assert add([2, 4, 3], [5, 6, 4]) == [7, 0, 8]
# assert add([1, 2, 3], [4, 5]) == [5, 7, 3]
# assert add([9], [9]) == [8, 1]
# assert add([9, 9, 9, 9], [9, 9, 9]) == [8, 9, 9, 0, 1]
# assert add([9] * 10 ** 4, [1]) == [0] * 10 ** 4 + [1]
# assert add([1] * 10 ** 4, [8] * 10 ** 4) == [9] * 10 ** 4
# assert add([5] * 10 ** 4, [5] * 10 ** 4) == [0] + [1] * (10 ** 4 - 1) + [1]
