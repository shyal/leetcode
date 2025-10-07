"""
URL: https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/description/

1290. Convert Binary Number in a Linked List to Integer

Given head, the head of a singly linked list. The value of each node in the linked list is either 0 or 1. The linked list holds the binary representation of a number.

Return the decimal value of the number in the linked list.

The most significant bit is at the head of the linked list.


Example 1:

Input: head = [1,0,1]
Output: 5
Explanation: (101) in base 2 = (5) in base 10

Example 2:

Input: head = [0]
Output: 0


Constraints:

    The Linked List is not empty.
    Number of nodes will not exceed 30.
    Each node's value is either 0 or 1.

---

Wondering if this can be done in O(1) extra space

1         0         1
2^2 * 1   2^1 * 0   2^0 * 1
4         0         1

Hmm might just built up a string.

"""


class Solution:
    def getDecimalValue(self, head: ListNode) -> int:
        it = head
        st = ""
        while it:
            st += "1" if it.val else "0"
            it = it.next
        return int(st, base=2)


sol = Solution()

# print(sol.getDecimalValue(build_linked_list([1, 0, 1])))  # 5

assert sol.getDecimalValue(build_linked_list([1, 0, 1])) == 5
assert sol.getDecimalValue(build_linked_list([0])) == 0
assert sol.getDecimalValue(build_linked_list([1])) == 1
assert sol.getDecimalValue(build_linked_list([1, 0])) == 2
assert sol.getDecimalValue(build_linked_list([0, 1])) == 1
assert sol.getDecimalValue(build_linked_list([1, 1, 1])) == 7
assert sol.getDecimalValue(build_linked_list([0, 0, 0])) == 0
assert sol.getDecimalValue(build_linked_list([1, 0, 1, 0])) == 10
