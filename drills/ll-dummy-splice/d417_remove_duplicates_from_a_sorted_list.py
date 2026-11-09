"""
EPI 7.8 Remove duplicates from a sorted list

Given the head L of a linked list sorted in nondecreasing order, remove
nodes so that each value appears once, and return the head. The list
may be empty.

Example 1:

Input: L = [2, 2, 3, 5, 7, 11, 11]
Output: [2, 3, 5, 7, 11]

Example 2:

Input: L = [4, 4, 4]
Output: [4]

Example 3:

Input: L = []
Output: []

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= Node.val <= 10^9
    L is sorted in nondecreasing order.

    REQUIRED: O(n) time, O(1) extra space. NO set, NO list of values,
    NO new nodes.
"""


class Solution:
    def remove_duplicates(self, L: ListNode | None) -> ListNode | None:
        pass


sol = Solution()

print(get_list_values(sol.remove_duplicates(build_linked_list([2, 2, 3, 5, 7, 11, 11]))))  # [2, 3, 5, 7, 11]


def nodes(h):
    out = []
    while h:
        out.append(h)
        h = h.next
    return out


def dedupe(vals):
    L = build_linked_list(vals)
    old = {id(n) for n in nodes(L)}
    head = sol.remove_duplicates(L)
    assert {id(n) for n in nodes(head)} <= old, "the result must use the input nodes"
    return get_list_values(head)


# assert dedupe([2, 2, 3, 5, 7, 11, 11]) == [2, 3, 5, 7, 11]
# assert dedupe([4, 4, 4]) == [4]
# assert dedupe([]) == []
# assert dedupe([1]) == [1]
# assert dedupe([1, 2]) == [1, 2]
# assert dedupe([1, 1]) == [1]
# assert dedupe([1, 1, 2]) == [1, 2]
# assert dedupe([1, 2, 2]) == [1, 2]
# assert dedupe([1, 2, 3, 4]) == [1, 2, 3, 4]
# assert dedupe([-3, -3, 0, 0, 0, 5, 9, 9]) == [-3, 0, 5, 9]
# assert dedupe([7] * 10 ** 5) == [7]
# assert dedupe(list(range(10 ** 5))) == list(range(10 ** 5))
# assert dedupe([v // 3 for v in range(10 ** 5)]) == list(range((10 ** 5 + 2) // 3))
