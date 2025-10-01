"""
URL: https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/description/?envType=study-plan-v2&envId=leetcode-75

2130. Maximum Twin Sum of a Linked List

In a linked list of size n, where n is even, the ith node (0-indexed) of the linked list is known as the twin of the (n-1-i)th node, if 0 <= i <= (n / 2) - 1.

        For example, if n = 4, then node 0 is the twin of node 3, and node 1 is the twin of node 2. These are the only nodes with twins for n = 4.

The twin sum is defined as the sum of a node and its twin.

Given the head of a linked list with even length, return the maximum twin sum of the linked list.


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

        The number of nodes in the list is an even integer in the range [2, 105].
        1 <= Node.val <= 105
"""

from typing import Optional
import linked_list_utils as llutils


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        it, prev, count = head, None, 0
        while it:
            count += 1
            it.prev = prev
            prev = it
            it = it.next

        right, left, _max = prev, head, 0
        while True:
            _max = max(_max, left.val + right.val)
            if left.next == right:
                break
            left, right = left.next, right.prev
        return _max


sol = Solution()

ll = llutils.build_linked_list([5, 4, 2, 1])
assert sol.pairSum(ll) == 6


ll = llutils.build_linked_list([4, 2, 2, 3])
assert sol.pairSum(ll) == 7


ll = llutils.build_linked_list([1, 2, 3, 4])
assert sol.pairSum(ll) == 5


ll = llutils.build_linked_list([5, 10, 1, 2])
assert sol.pairSum(ll) == 11


ll = llutils.build_linked_list([1, 100, 1, 1])
assert sol.pairSum(ll) == 101


ll = llutils.build_linked_list([100000, 1, 1, 100000])
assert sol.pairSum(ll) == 200000


ll = llutils.build_linked_list([1, 1, 1, 1])
assert sol.pairSum(ll) == 2


ll = llutils.build_linked_list([1, 100000])
assert sol.pairSum(ll) == 100001
