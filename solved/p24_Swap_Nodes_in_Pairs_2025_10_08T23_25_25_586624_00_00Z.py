"""
URL: https://leetcode.com/problems/swap-nodes-in-pairs/description/

24. Swap Nodes in Pairs

Given the head of a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)


Example 1:

Input: head = [1,2,3,4]
Output: [2,1,4,3]

Example 2:

Input: head = []
Output: []

Example 3:

Input: head = [1]
Output: [1]


Constraints:

    The number of nodes in the list is in the range [0, 100].
    0 <= Node.val <= 100

---

Could only get it to work with an odd number of nodes.
Looked up a recursive solution. It's neat.

"""


class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        # credit: https://leetcode.com/problems/swap-nodes-in-pairs/solutions/557411/python-recursive-solution-faster-than-99-72/
        if head:
            h = head.next
            if h:
                h.next, head.next = (
                    head,
                    h.next,
                )
                h.next.next = self.swapPairs(h.next.next)
                return h
        return head


sol = Solution()

# ll = build_linked_list([1, 2, 3, 4])
# draw_linked_list(ll)
# print(get_list_values(sol.swapPairs(ll)))  # [2,1,4,3]

assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3, 4]))) == [2, 1, 4, 3]
assert get_list_values(sol.swapPairs(build_linked_list([]))) == []
assert get_list_values(sol.swapPairs(build_linked_list([1]))) == [1]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2]))) == [2, 1]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3]))) == [2, 1, 3]
assert get_list_values(sol.swapPairs(build_linked_list([1, 2, 3, 4, 5]))) == [
    2,
    1,
    4,
    3,
    5,
]
assert get_list_values(sol.swapPairs(build_linked_list([0, 0, 0]))) == [0, 0, 0]
assert get_list_values(sol.swapPairs(build_linked_list([100, 0, 100, 0]))) == [
    0,
    100,
    0,
    100,
]
