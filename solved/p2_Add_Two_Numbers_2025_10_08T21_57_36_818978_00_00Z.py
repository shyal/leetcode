"""
URL: https://leetcode.com/problems/add-two-numbers/description/

2. Add Two Numbers

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

Constraints:

    The number of nodes in each linked list is in the range [1, 100].
    0 <= Node.val <= 9
    It is guaranteed that the list represents a number that does not have leading zeros.

---

Create the dummy head of a new list.
Create two it pointers for each list.
While there's an it pointer that's still valid and there's no carry.
Add both pointer values. divmod.
Create new list node, and connect previous to this node.
Set remaining to node
set carry to div.

"""


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
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
        return dummy.next


sol = Solution()

# l1 = build_linked_list([2, 4, 3])
# l2 = build_linked_list([5, 6, 4])
# print(get_list_values(sol.addTwoNumbers(l1, l2)))  # [7,0,8]

assert get_list_values(
    sol.addTwoNumbers(build_linked_list([2, 4, 3]), build_linked_list([5, 6, 4]))
) == [7, 0, 8]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([0]), build_linked_list([0]))
) == [0]
assert get_list_values(
    sol.addTwoNumbers(
        build_linked_list([9, 9, 9, 9, 9, 9, 9]), build_linked_list([9, 9, 9, 9])
    )
) == [8, 9, 9, 9, 0, 0, 0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([0]), build_linked_list([1]))
) == [1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1]), build_linked_list([0]))
) == [1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9]), build_linked_list([1]))
) == [0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([5]), build_linked_list([5]))
) == [0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1, 2, 3]), build_linked_list([4, 5, 6]))
) == [5, 7, 9]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9, 9, 9]), build_linked_list([1, 0, 0]))
) == [0, 0, 0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([0, 0, 1]), build_linked_list([9, 9, 9]))
) == [9, 9, 0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1, 2, 3, 4, 5]), build_linked_list([9, 9]))
) == [0, 2, 4, 4, 5]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([1, 2, 3]), build_linked_list([1, 2, 3]))
) == [2, 4, 6]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9, 5]), build_linked_list([1, 6]))
) == [0, 2, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([9, 9]), build_linked_list([1]))
) == [0, 0, 1]
assert get_list_values(
    sol.addTwoNumbers(build_linked_list([0]), build_linked_list([1, 2, 3]))
) == [1, 2, 3]
