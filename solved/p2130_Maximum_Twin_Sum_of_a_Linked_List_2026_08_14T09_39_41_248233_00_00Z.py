"""
URL: https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/description/?envType=problem-list-v2&envId=vn57k9wr

2130. Maximum Twin Sum of a Linked List

In a linked list of size n, where n is even, the ith node (0-indexed) of the
linked list is known as the twin of the (n-1-i)th node, if 0 <= i <= (n / 2) - 1.

    For example, if n = 4, then node 0 is the twin of node 3, and node 1 is the
    twin of node 2. These are the only nodes with twins for n = 4.

The twin sum is defined as the sum of a node and its twin.

Given the head of a linked list with even length, return the maximum twin sum
of the linked list.


Example 1:

Input: head = [5,4,2,1]
Output: 6
Explanation:
Nodes 0 and 1 are the twins of nodes 3 and 2, respectively. All have twin sum = 6.
There are no other nodes with twins in the linked list.
Thus, the maximum twin sum of the linked list is 6.

Example 2:

Input: head = [4,2,2,3]
Output: 7
Explanation:
The nodes with twins present in this linked list are:
- Node 0 is the twin of node 3 having a twin sum of 4 + 3 = 7.
- Node 1 is the twin of node 2 having a twin sum of 2 + 2 = 4.
Thus, the maximum twin sum of the linked list is max(7, 4) = 7.

Example 3:

Input: head = [1,100000]
Output: 100001
Explanation:
There is only one node with a twin in the linked list having twin sum of 1 + 100000 = 100001.


Constraints:

    The number of nodes in the list is an even integer in the range [2, 10^5].
    1 <= Node.val <= 10^5

---

Rusty, and since i'd perfected my `reverseSublist` in the past, i decided
to peek at it, and create a mnemonic for it. No point rederiving a perfectly
good helper function.
"""
class Solution:

    def reverseSublist(self, head):
        d = ListNode()
        tail = head
        while head:
            d.next, head.next, head = head, d.next, head.next
        return d.next, tail

    def pairSum(self, head: Optional[ListNode]) -> int:
        fast, slow = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow
        a, b = self.reverseSublist(second)
        # print_linked_list(a)
        # print_linked_list(head)
        twin_sum = 0
        while a:
            twin_sum = max(twin_sum, head.val + a.val)
            head = head.next
            a = a.next
        return twin_sum
        
        


sol = Solution()

assert sol.pairSum(build_linked_list([5, 4, 2, 1])) == 6
assert sol.pairSum(build_linked_list([4, 2, 2, 3])) == 7
assert sol.pairSum(build_linked_list([1, 100000])) == 100001
assert sol.pairSum(build_linked_list([1, 1])) == 2
assert sol.pairSum(build_linked_list([100000, 100000])) == 200000
assert sol.pairSum(build_linked_list([1, 2, 3, 4, 5, 6])) == 7
assert sol.pairSum(build_linked_list([1, 1, 1, 1, 1, 1])) == 2
assert sol.pairSum(build_linked_list([2, 1, 1, 9])) == 11
assert sol.pairSum(build_linked_list([1, 2, 2, 1])) == 4
assert sol.pairSum(build_linked_list([1, 9, 9, 1])) == 18
assert sol.pairSum(build_linked_list([9, 1, 1, 1, 1, 1])) == 10
assert sol.pairSum(build_linked_list([1, 1, 1, 1, 1, 9])) == 10
assert sol.pairSum(build_linked_list([1, 2, 3, 4, 4, 3, 2, 1])) == 8
assert sol.pairSum(build_linked_list([1, 5, 3, 2, 6, 8])) == 11
assert sol.pairSum(build_linked_list([47, 53, 42, 199, 123, 200])) == 247
assert sol.pairSum(build_linked_list(list(range(1, 11)))) == 11