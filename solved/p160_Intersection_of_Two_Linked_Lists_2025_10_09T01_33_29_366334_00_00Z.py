"""
URL: https://leetcode.com/problems/intersection-of-two-linked-lists/description/

160. Intersection of Two Linked Lists

Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.

For example, the following two linked lists begin to intersect at node c1:

A:       a1 → a2
           ↘
             c1 → c2 → c3
           ↗
B: b1 → b2 → b3

The test cases are generated such that there are no cycles anywhere in the entire linked structure.

Note that the linked lists must retain their original structure after the function returns.

Custom Judge:

The inputs to the judge are given as follows (your program is not given these inputs):

    intersectVal - The value of the node where the intersection occurs. This is 0 if there is no intersecting node.
    listA - The first linked list.
    listB - The second linked list.
    skipA - The number of nodes to skip ahead in listA (starting from the head) to get to the intersected node.
    skipB - The number of nodes to skip ahead in listB (starting from the head) to get to the intersected node.

The judge will then create the linked structure based on these inputs and pass the two heads, headA and headB to your program. If you correctly return the intersected node, then your solution will be accepted.

Example 1:

Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
Output: Intersected at '8'
Explanation: The intersected node's value is 8 (note that this must not be 0 if the two lists intersect).
From the head of A, it reads as [4,1,8,4,5]. From the head of B, it reads as [5,6,1,8,4,5]. There are 2 nodes before the intersected node in A; There are 3 nodes before the intersected node in B.

Example 2:

Input: intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
Output: Intersected at '2'
Explanation: The intersected node's value is 2 (note that this must not be 0 if the two lists intersect).
From the head of A, it reads as [1,9,1,2,4]. From the head of B, it reads as [3,2,4]. There are 3 nodes before the intersected node in A; There are 1 node before the intersected node in B.

Example 3:

Input: intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
Output: No intersection
Explanation: From the head of A, it reads as [2,6,4]. From the head of B, it reads as [1,5]. Since the two lists do not intersect, intersectVal must be 0, while skipA and skipB can be arbitrary values.
Explanation: The two lists do not intersect, so return null.

Constraints:

    The number of nodes of listA is in the m.
    The number of nodes of listB is in the n.
    1 <= m, n <= 3 * 10^4
    1 <= Node.val <= 10^5
    0 <= skipA < m
    0 <= skipB < n
    intersectVal is 0 if listA and listB do not intersect.
    intersectVal == listA[skipA] == listB[skipB] if listA and listB intersect.

Follow up: Could you write a solution that runs in O(m + n) time and use only O(1) memory?

---

Ok i'll try the follow up version.

Algo:

- get length of both lists, i.e n1 and n2
- calc diff, i.e 2
- advance longest list by diff
- iterate both lists until pointers meet

"""


class Solution:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:
        def listLength(head):
            count = 0
            while head:
                count += 1
                head = head.next
            return count

        a_length = listLength(headA)
        b_length = listLength(headB)

        diff = abs(a_length - b_length)

        diff_it = (headB, headA)[a_length > b_length]

        for _ in range(diff):
            diff_it = diff_it.next

        if a_length > b_length:
            headA = diff_it
        else:
            headB = diff_it

        while headA != headB:
            headA = headA.next
            headB = headB.next

        return headA


sol = Solution()

# Example 1
common = build_linked_list([8, 4, 5])
listA = build_linked_list([4, 1])
listA.next.next = common
listB = build_linked_list([5, 6, 1])
listB.next.next.next = common
intersection = sol.getIntersectionNode(listA, listB)
# print(intersection.val if intersection else None)  # 8

# Example 1 assert
common = build_linked_list([8, 4, 5])
listA = build_linked_list([4, 1])
listA.next.next = common
listB = build_linked_list([5, 6, 1])
listB.next.next.next = common
assert sol.getIntersectionNode(listA, listB) == common

# Example 2
common = build_linked_list([2, 4])
listA = build_linked_list([1, 9, 1])
listA.next.next.next = common
listB = build_linked_list([3])
listB.next = common
assert sol.getIntersectionNode(listA, listB) == common

# Example 3
listA = build_linked_list([2, 6, 4])
listB = build_linked_list([1, 5])
assert sol.getIntersectionNode(listA, listB) == None

common = build_linked_list([1, 2, 3])
listA = common
listB = common
assert sol.getIntersectionNode(listA, listB) == common

common = build_linked_list([1, 2, 3])
listB = build_linked_list([4, 5])
tmp = listB
while tmp.next:
    tmp = tmp.next
tmp.next = common
listA = common
assert sol.getIntersectionNode(listA, listB) == common

common = build_linked_list([1, 2, 3])
listA = build_linked_list([4, 5])
tmp = listA
while tmp.next:
    tmp = tmp.next
tmp.next = common
listB = common
assert sol.getIntersectionNode(listA, listB) == common

listA = build_linked_list([1, 2, 3])
listB = build_linked_list([1, 2, 3])
assert sol.getIntersectionNode(listA, listB) is None

node = ListNode(1)
assert sol.getIntersectionNode(node, node) == node

listA = ListNode(1)
listB = ListNode(1)
assert sol.getIntersectionNode(listA, listB) is None

common = build_linked_list([3, 4, 5])
listA = build_linked_list([1, 2])
listA.next.next = common
listB = common.next
assert sol.getIntersectionNode(listA, listB) == listB

listA = None
listB = build_linked_list([1])
assert sol.getIntersectionNode(listA, listB) is None

listA = build_linked_list([1])
listB = None
assert sol.getIntersectionNode(listA, listB) is None

assert sol.getIntersectionNode(None, None) is None
