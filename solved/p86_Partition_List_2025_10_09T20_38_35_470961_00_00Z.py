"""
URL: https://leetcode.com/problems/partition-list/description/?envType=study-plan-v2&envId=top-interview-150

86. Partition List

Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.

You should preserve the original relative order of the nodes in each of the two partitions.

Example 1:

Input: head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]

Example 2:

Input: head = [2,1], x = 2
Output: [1,2]

Constraints:

    The number of nodes in the list is in the range [0, 200].
    -100 <= Node.val <= 100
    -200 <= x <= 200

"""


class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        d = ListNode("dummy")
        d.next = head
        gt_head = ListNode("gt")
        gt_it = gt_head
        it = d
        while it.next:
            if it.next.val >= x:
                gt_it.next = it.next
                gt_it = gt_it.next
                it.next = it.next.next
                gt_it.next = None
            else:
                it = it.next

        # draw_linked_list(d)
        # draw_linked_list(gt_head)

        it.next = gt_head.next
        # draw_linked_list(d)
        return d.next


sol = Solution()

# print(
    get_list_values(sol.partition(build_linked_list([1, 4, 3, 2, 5, 2]), 3))
)  # [1, 2, 2, 4, 3, 5]

assert get_list_values(sol.partition(build_linked_list([1, 4, 3, 2, 5, 2]), 3)) == [
    1,
    2,
    2,
    4,
    3,
    5,
]
assert get_list_values(sol.partition(build_linked_list([2, 1]), 2)) == [1, 2]
assert get_list_values(sol.partition(build_linked_list([]), 3)) == []
assert get_list_values(sol.partition(build_linked_list([1]), 2)) == [1]
assert get_list_values(sol.partition(build_linked_list([2]), 2)) == [2]
assert get_list_values(sol.partition(build_linked_list([3]), 2)) == [3]
assert get_list_values(sol.partition(build_linked_list([1, 2, 3]), 4)) == [1, 2, 3]
assert get_list_values(sol.partition(build_linked_list([4, 5, 6]), 3)) == [4, 5, 6]
assert get_list_values(sol.partition(build_linked_list([3, 1, 2]), 3)) == [1, 2, 3]
assert get_list_values(sol.partition(build_linked_list([-1, -5, 0, 2, -3]), -2)) == [
    -5,
    -3,
    -1,
    0,
    2,
]
assert get_list_values(sol.partition(build_linked_list([5, 5, 5]), 5)) == [5, 5, 5]
assert get_list_values(sol.partition(build_linked_list([1, -1, 2, -2]), 0)) == [
    -1,
    -2,
    1,
    2,
]
assert get_list_values(sol.partition(build_linked_list([-100]), -200)) == [-100]
assert get_list_values(sol.partition(build_linked_list([100]), 200)) == [100]
