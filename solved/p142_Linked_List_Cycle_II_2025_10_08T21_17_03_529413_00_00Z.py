"""
URL: https://leetcode.com/problems/linked-list-cycle-ii/description/

142. Linked List Cycle II

Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.

Do not modify the linked list.

Example 1:

Input: head = [3,2,0,-4], pos = 1
Output: tail connects to node index 1
Explanation: There is a cycle in the linked list, where tail connects to the second node.

Example 2:

Input: head = [1,2], pos = 0
Output: tail connects to node index 0
Explanation: There is a cycle in the linked list, where tail connects to the first node.

Example 3:

Input: head = [1], pos = -1
Output: no cycle
Explanation: There is no cycle in the linked list.

Constraints:

    The number of the nodes in the list is in the range [0, 10^4].
    -10^5 <= Node.val <= 10^5
    pos is -1 or a valid index in the linked-list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?

---

- Slow and fast pointers start on head
- Slow iterates by 1, Fast by 2
- When they meet, set slow to head
- Iterate them together until they meet

"""


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return
        slow, fast = head, head
        has_cycle = False
        while slow and fast and slow.next and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                has_cycle = True
                break

        if not has_cycle:
            return

        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        return slow


sol = Solution()

nodes1 = [ListNode(3), ListNode(2), ListNode(0), ListNode(-4)]
for i in range(3):
    nodes1[i].next = nodes1[i + 1]
nodes1[3].next = nodes1[1]
head1 = nodes1[0]
result1 = sol.detectCycle(head1)

nodes1 = [ListNode(3), ListNode(2), ListNode(0), ListNode(-4)]
for i in range(3):
    nodes1[i].next = nodes1[i + 1]
nodes1[3].next = nodes1[1]
head1 = nodes1[0]
assert sol.detectCycle(head1) == nodes1[1]

nodes2 = [ListNode(1), ListNode(2)]
nodes2[0].next = nodes2[1]
nodes2[1].next = nodes2[0]
head2 = nodes2[0]
assert sol.detectCycle(head2) == nodes2[0]

# Example 3 assert
nodes3 = [ListNode(1)]
head3 = nodes3[0]
assert sol.detectCycle(head3) is None

assert sol.detectCycle(None) is None

node4 = ListNode(1)
node4.next = node4
assert sol.detectCycle(node4) == node4

nodes5 = [ListNode(1), ListNode(2)]
nodes5[0].next = nodes5[1]
assert sol.detectCycle(nodes5[0]) is None

nodes6 = [ListNode(1), ListNode(2), ListNode(3)]
for i in range(2):
    nodes6[i].next = nodes6[i + 1]
nodes6[2].next = nodes6[0]
assert sol.detectCycle(nodes6[0]) == nodes6[0]

nodes7 = [ListNode(1), ListNode(2), ListNode(3)]
for i in range(2):
    nodes7[i].next = nodes7[i + 1]
nodes7[2].next = nodes7[1]
assert sol.detectCycle(nodes7[0]) == nodes7[1]

nodes8 = [ListNode(1), ListNode(2)]
nodes8[0].next = nodes8[1]
nodes8[1].next = nodes8[1]
assert sol.detectCycle(nodes8[0]) == nodes8[1]

nodes9 = [ListNode(i) for i in range(5)]
for i in range(4):
    nodes9[i].next = nodes9[i + 1]
assert sol.detectCycle(nodes9[0]) is None

nodes10 = [ListNode(1), ListNode(-1), ListNode(0), ListNode(100000)]
for i in range(3):
    nodes10[i].next = nodes10[i + 1]
nodes10[3].next = nodes10[2]
assert sol.detectCycle(nodes10[0]) == nodes10[2]

nodes11 = [ListNode(0) for _ in range(3)]
for i in range(2):
    nodes11[i].next = nodes11[i + 1]
nodes11[2].next = nodes11[0]
assert sol.detectCycle(nodes11[0]) == nodes11[0]

#                                  0.   1. 2.  3.  4. 5.  6.  7.  8.  9
nodes = [ListNode(val) for val in [-1, -7, 7, -4, 19, 6, -9, -5, -2, -5]]
for i in range(9):
    nodes[i].next = nodes[i + 1]
nodes[9].next = nodes[9]
head = nodes[0]

result = sol.detectCycle(head)
expected = nodes[9]
assert (
    result == expected
), f"Expected node with value {expected.val} at index 9, but got node with value {result.val if result else None}"
