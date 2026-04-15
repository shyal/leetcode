"""
URL: https://leetcode.com/problems/linked-list-cycle/description/?envType=problem-list-v2&envId=vn57k9wr

141. Linked List Cycle

Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

Example 1:

Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

Example 2:

Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.

Example 3:

Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.

Constraints:

- The number of the nodes in the list is in the range [0, 10^4].
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?
"""


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head
        i = 0
        while slow and fast and fast.next:
            i += 1
            slow = slow.next
            fast = fast.next.next
            if fast is None:
                return False
            if slow.val == fast.val:
                print('loop detected', slow.val)
                return True
            if i > 10**4:
                return False
        return False



sol = Solution()

# First example
vals = [3, 2, 0, -4]
pos = 1
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
print(print_linked_list(head))
print(sol.hasCycle(head))  # true


vals = [1, 2]
pos = 0
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
print_linked_list(head)
assert sol.hasCycle(head) == True

vals = [1]
pos = -1
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
print_linked_list(head)
assert sol.hasCycle(head) == False

vals = []
pos = -1
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
assert sol.hasCycle(head) == False

vals = [1]
pos = 0
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
assert sol.hasCycle(head) == True

vals = [1, 2]
pos = -1
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
assert sol.hasCycle(head) == False

vals = [1, 2, 3, 4]
pos = 2
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
assert sol.hasCycle(head) == True

vals = [1, 2, 3, 4, 5]
pos = -1
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
assert sol.hasCycle(head) == False


vals = [1, 2, 3, 4]
pos = 0
head = build_linked_list(vals)
if pos != -1:
    tail = head
    while tail.next:
        tail = tail.next
    node = head
    for _ in range(pos):
        node = node.next
    tail.next = node
assert sol.hasCycle(head) == True