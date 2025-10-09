"""
URL: https://leetcode.com/problems/add-two-numbers-ii/description/?envType=problem-list-v2&envId=linked-list

445. Add Two Numbers II

You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:

Input: l1 = [7,2,4,3], l2 = [5,6,4]
Output: [7,8,0,7]

Example 2:

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [8,0,7]

Example 3:

Input: l1 = [0], l2 = [0]
Output: [0]

Constraints:

    The number of nodes in each linked list is in the range [1, 100].
    0 <= Node.val <= 9
    It is guaranteed that the list represents a number that does not have leading zeros.
"""


class Solution:

    def reverse(self, head):
        d = ListNode(-1)
        while head:
            d.next, head.next, head = head, d.next, head.next
        return d.next

    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        l1 = self.reverse(l1)
        l2 = self.reverse(l2)
        dummy = ListNode()
        carry = 0
        it = dummy
        while l1 or l2 or carry:
            val = carry
            if l1:
                val += l1.val
                l1 = l1.next
            if l2:
                val += l2.val
                l2 = l2.next
            carry, mod = divmod(val, 10)
            it.next = ListNode(mod)
            it = it.next
        return self.reverse(dummy.next)


sol = Solution()

# print(
#     get_list_values(
#         sol.addTwoNumbers(build_linked_list([7, 2, 4, 3]), build_linked_list([5, 6, 4]))
#     )
# )  # [7,8,0,7]

assert get_list_values(
    sol.addTwoNumbers(build_linked_list([7, 2, 4, 3]), build_linked_list([5, 6, 4]))
) == [7, 8, 0, 7]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([2, 4, 3]), build_linked_list([5, 6, 4]))
) == [8, 0, 7]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([0]), build_linked_list([0]))
) == [0]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9, 9, 9]), build_linked_list([1]))
) == [1, 0, 0, 0]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1]), build_linked_list([9, 9, 9]))
) == [1, 0, 0, 0]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([5]), build_linked_list([5]))
) == [1, 0]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([0]), build_linked_list([1]))
) == [1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1, 0, 0]), build_linked_list([0]))
) == [1, 0, 0]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1, 2, 3]), build_linked_list([4, 5, 6]))
) == [5, 7, 9]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1]), build_linked_list([9, 9, 9, 9]))
) == [1, 0, 0, 0, 0]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([3]), build_linked_list([4]))
) == [7]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9]), build_linked_list([9]))
) == [1, 8]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9, 9, 9, 9]), build_linked_list([9, 9, 9, 9]))
) == [1, 9, 9, 9, 8]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1, 0, 0, 0, 0]), build_linked_list([1]))
) == [1, 0, 0, 0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([2, 4]), build_linked_list([3]))
) == [2, 7]
