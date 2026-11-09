"""
EPI 7.1 Merge two sorted lists

Given the heads L1 and L2 of two linked lists, each sorted in
nondecreasing order, return the head of a single sorted list made of
the nodes of L1 and L2. Either list may be empty.

Example 1:

Input: L1 = [2, 5, 7], L2 = [3, 11]
Output: [2, 3, 5, 7, 11]

Example 2:

Input: L1 = [], L2 = [1, 2]
Output: [1, 2]

Example 3:

Input: L1 = [4, 4], L2 = [4]
Output: [4, 4, 4]

Constraints:

    0 <= number of nodes in L1, L2 <= 5 * 10^4
    -10^9 <= Node.val <= 10^9
    L1 and L2 are each sorted in nondecreasing order.

    REQUIRED: O(n + m) time, O(1) extra space. NO list of values, NO
    sorting, NO recursion.
"""


class Solution:
    def merge_two_sorted_lists(
        self, L1: ListNode | None, L2: ListNode | None
    ) -> ListNode | None:
        pass


sol = Solution()

print(get_list_values(sol.merge_two_sorted_lists(build_linked_list([2, 5, 7]), build_linked_list([3, 11]))))  # [2, 3, 5, 7, 11]


def nodes(h):
    out = []
    while h:
        out.append(h)
        h = h.next
    return out


def merge(a, b):
    L1, L2 = build_linked_list(a), build_linked_list(b)
    old = {id(n) for n in nodes(L1) + nodes(L2)}
    head = sol.merge_two_sorted_lists(L1, L2)
    assert {id(n) for n in nodes(head)} == old, "the result must use the input nodes"
    return get_list_values(head)


# assert merge([2, 5, 7], [3, 11]) == [2, 3, 5, 7, 11]
# assert merge([], [1, 2]) == [1, 2]
# assert merge([1, 2], []) == [1, 2]
# assert merge([], []) == []
# assert merge([4, 4], [4]) == [4, 4, 4]
# assert merge([1], [2]) == [1, 2]
# assert merge([2], [1]) == [1, 2]
# assert merge([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
# assert merge([4, 5, 6], [1, 2, 3]) == [1, 2, 3, 4, 5, 6]
# assert merge([1, 3, 5, 7], [2, 4, 6, 8]) == [1, 2, 3, 4, 5, 6, 7, 8]
# assert merge([-10 ** 9, 0], [-5, 10 ** 9]) == [-10 ** 9, -5, 0, 10 ** 9]
# assert merge([1, 1, 2], [1, 2, 2]) == [1, 1, 1, 2, 2, 2]
# assert merge(list(range(0, 10 ** 5, 2)), list(range(1, 10 ** 5, 2))) == list(range(10 ** 5))
# assert merge(list(range(5 * 10 ** 4)), [-1]) == [-1] + list(range(5 * 10 ** 4))
