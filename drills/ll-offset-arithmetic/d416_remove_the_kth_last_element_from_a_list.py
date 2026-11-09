"""
EPI 7.7 Remove the kth last element from a list

Given the head L of a linked list and an integer k, remove the kth node
from the end of the list and return the head. The tail is the 1st node
from the end.

Example 1:

Input: L = [1, 2, 3, 4, 5], k = 2
Output: [1, 2, 3, 5]

Example 2:

Input: L = [1, 2], k = 2
Output: [2]
Explanation: the 2nd node from the end is the head.

Example 3:

Input: L = [7], k = 1
Output: []

Constraints:

    1 <= k <= n <= 10^5, where n is the number of nodes in L
    -10^9 <= Node.val <= 10^9

    REQUIRED: O(n) time, O(1) extra space, one pass over the list. NO
    count of the nodes, NO list of nodes.
"""


class Solution:
    def remove_kth_last(self, L: ListNode, k: int) -> ListNode | None:
        pass


sol = Solution()

print(get_list_values(sol.remove_kth_last(build_linked_list([1, 2, 3, 4, 5]), 2)))  # [1, 2, 3, 5]


def remove(vals, k):
    return get_list_values(sol.remove_kth_last(build_linked_list(vals), k))


# assert remove([1, 2, 3, 4, 5], 2) == [1, 2, 3, 5]
# assert remove([1, 2], 2) == [2]
# assert remove([1, 2], 1) == [1]
# assert remove([7], 1) == []
# assert remove([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4]
# assert remove([1, 2, 3, 4, 5], 5) == [2, 3, 4, 5]
# assert remove([1, 2, 3, 4, 5], 3) == [1, 2, 4, 5]
# assert remove([1, 2, 3], 2) == [1, 3]
# assert remove([5, 5, 5, 6], 4) == [5, 5, 6]
# assert remove([5, 5, 5, 6], 1) == [5, 5, 5]
# assert remove(list(range(10 ** 5)), 1) == list(range(10 ** 5 - 1))
# assert remove(list(range(10 ** 5)), 10 ** 5) == list(range(1, 10 ** 5))
# assert remove(list(range(10 ** 5)), 5 * 10 ** 4) == [v for v in range(10 ** 5) if v != 5 * 10 ** 4]
