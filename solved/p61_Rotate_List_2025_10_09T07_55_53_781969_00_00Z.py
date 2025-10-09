"""
URL: https://leetcode.com/problems/rotate-list/description/?envType=study-plan-v2&envId=top-interview-150

61. Rotate List

Given the head of a linked list, rotate the list to the right by k places.

Example 1:

Input: head = [1,2,3,4,5], k = 2
Output: [4,5,1,2,3]

Example 2:

Input: head = [0,1,2], k = 4
Output: [2,0,1]

Constraints:

    The number of nodes in the list is in the range [0, 500].
    -100 <= Node.val <= 100
    0 <= k <= 2 * 10^9
"""


class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return
        if not head:
            return []
        if not head.next:
            return head
        if k == 0:
            return head
        count = 0
        it = head
        while it:
            count += 1
            it = it.next
        shift_by = count - (k % count)
        if k % count == 0:
            return head
        it = head
        for _ in range(shift_by - 1):
            it = it.next
        cont = it.next
        if it:
            it.next = None

        new_head = cont

        while cont:
            if cont.next:
                cont = cont.next
            else:
                cont.next = head
                break
        return new_head


sol = Solution()

# print_linked_list(sol.rotateRight(build_linked_list([1, 2, 3, 4, 5]), 2))  # [4,5,1,2,3]

assert get_list_values(sol.rotateRight(build_linked_list([1, 2, 3, 4, 5]), 10)) == [
    1,
    2,
    3,
    4,
    5,
]

assert get_list_values(sol.rotateRight(build_linked_list([1, 2, 3, 4, 5]), 2)) == [
    4,
    5,
    1,
    2,
    3,
]
assert get_list_values(sol.rotateRight(build_linked_list([0, 1, 2]), 4)) == [2, 0, 1]
assert get_list_values(sol.rotateRight(build_linked_list([]), 0)) == []
assert get_list_values(sol.rotateRight(build_linked_list([]), 1)) == []
assert get_list_values(sol.rotateRight(build_linked_list([]), 1000000000)) == []
assert get_list_values(sol.rotateRight(build_linked_list([1]), 0)) == [1]
assert get_list_values(sol.rotateRight(build_linked_list([1]), 1)) == [1]
assert get_list_values(sol.rotateRight(build_linked_list([1]), 1000000000)) == [1]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2]), 0)) == [1, 2]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2]), 1)) == [2, 1]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2]), 2)) == [1, 2]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2]), 3)) == [2, 1]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2, 3]), 1)) == [3, 1, 2]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2, 3]), 2)) == [2, 3, 1]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2, 3]), 3)) == [1, 2, 3]
assert get_list_values(sol.rotateRight(build_linked_list([1, 2, 3]), 4)) == [3, 1, 2]
assert get_list_values(sol.rotateRight(build_linked_list([-1, 0, 1]), 2)) == [0, 1, -1]
