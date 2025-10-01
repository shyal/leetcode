"""
URL: https://leetcode.com/problems/palindrome-linked-list/description/

234. Palindrome Linked List

Given the head of a singly linked list, return true if it is a palindrome or false otherwise.


Example 1:

Input: head = [1,2,2,1]
Output: true

Example 2:

Input: head = [1,2]
Output: false


Constraints:

    The number of nodes in the list is in the range [1, 105].
    0 <= Node.val <= 9


Follow up: Could you do it in O(n) time and O(1) space?
"""


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        it = head
        prev = None
        while it:
            it.prev = prev
            prev = it
            it = it.next
        it = head
        end = prev
        while it != end:
            if end.val != it.val:
                return False
            if it.next == end or end.prev == it:
                return it.next.val == end.prev.val
            it = it.next
            end = end.prev
        return True


sol = Solution()

head = build_linked_list([1, 2, 2, 1])
# draw_linked_list(head)
assert sol.isPalindrome(head) == True

head = build_linked_list([1, 2])
# draw_linked_list(head)
assert sol.isPalindrome(head) == False

head = build_linked_list([1, 2, 1])
# draw_linked_list(head)
assert sol.isPalindrome(head) == True


head = build_linked_list([1, 2, 3, 2, 1])
# draw_linked_list(head)
assert sol.isPalindrome(head) == True


head = build_linked_list([1, 1, 3, 2, 1])
# draw_linked_list(head)
assert sol.isPalindrome(head) == False


head = build_linked_list([1, 1, 1, 1, 1, 1, 1, 1])
# draw_linked_list(head)
assert sol.isPalindrome(head) == True
