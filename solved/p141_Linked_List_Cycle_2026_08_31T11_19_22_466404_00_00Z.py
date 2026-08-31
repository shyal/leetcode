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

    The number of the nodes in the list is in the range [0, 10^4].
    -10^5 <= Node.val <= 10^5
    pos is -1 or a valid index in the linked-list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?


---


1    2.    3.
                4

       7        5
            6

"""


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head

        has_cycle = False

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                print("cycle")
                has_cycle = True
                break
        return has_cycle


sol = Solution()

# Example 1
head1 = build_linked_list([3, 2, 0, -4])

print(head1)

# Create cycle pos=1 (0-indexed)
tail = head1
while tail.next:
    tail = tail.next
second_node = head1.next
tail.next = second_node
print(sol.hasCycle(head1))  # True

# Example 2
head2 = build_linked_list([1, 2])
tail = head2
while tail.next:
    tail = tail.next
tail.next = head2  # pos=0
assert sol.hasCycle(head2) is True

# Example 3
head3 = build_linked_list([1])
assert sol.hasCycle(head3) is False

# Additional asserts for empty list and single node no cycle
assert sol.hasCycle(None) is False
single_node = ListNode(1)
assert sol.hasCycle(single_node) is False
