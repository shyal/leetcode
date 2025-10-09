"""
URL: https://leetcode.com/problems/reverse-linked-list-ii/description/?envType=problem-list-v2&envId=vn57k9wr

92. Reverse Linked List II

Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.

Example 1:

Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]

Example 2:

Input: head = [5], left = 1, right = 1
Output: [5]

Constraints:

    The number of nodes in the list is in the range [1, 500].
    -500 <= Node.val <= 500
    1 <= left <= right <= n, where n is the length of the list.

Follow up: Could you do it in one pass?

---

Ran out of time.

Came up with a not so great solution, which passed some of the test cases.
Ran out of time, so looked at a solution.

The main insight that really annoyed me missing is that the node values are labelled
1, 2, 3, 4, 5 which means i can iterate using ranges, using left, right, right - left
etc.

Also I need more practice reversing a linked list.

"""


class Solution:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:

        if not head or left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy

        for _ in range(left - 1):
            prev = prev.next

        cur = prev.next
        for _ in range(right - left):
            temp = cur.next
            cur.next = temp.next
            temp.next = prev.next
            prev.next = temp

        return dummy.next


sol = Solution()

# print(
#     get_list_values(sol.reverseBetween(build_linked_list([1, 2, 3, 4, 5]), 2, 4))
# )  # [1, 4, 3, 2, 5]

assert get_list_values(
    sol.reverseBetween(build_linked_list([1, 2, 3, 4, 5]), 2, 4)
) == [1, 4, 3, 2, 5]
assert get_list_values(sol.reverseBetween(build_linked_list([5]), 1, 1)) == [5]
assert get_list_values(
    sol.reverseBetween(build_linked_list([1, 2, 3, 4, 5]), 1, 5)
) == [5, 4, 3, 2, 1]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2,3,4,5]), 1, 2)) == [2, 1, 3, 4, 5]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2,3,4,5]), 4, 5)) == [1, 2, 3, 5, 4]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2,3,4,5]), 3, 3)) == [1, 2, 3, 4, 5]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2]), 1, 2)) == [2, 1]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2]), 1, 1)) == [1, 2]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2]), 2, 2)) == [1, 2]
# assert get_list_values(sol.reverseBetween(build_linked_list([3, -1, 4]), 1, 3)) == [4, -1, 3]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2,3,4,5,6,7]), 3, 6)) == [1, 2, 6, 5, 4, 3, 7]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2,3]), 1, 1)) == [1, 2, 3]
# assert get_list_values(sol.reverseBetween(build_linked_list([1,2,3]), 3, 3)) == [1, 2, 3]
