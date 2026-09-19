"""
DRILL: Interleave

Given the heads a and b of two linked lists, where b has as many nodes as
a or one fewer, weave them into one list that alternates a node of a and
a node of b, starting with a, and return its head. The nodes move; no
node is created.

Example 1:

Input: a = [1, 2, 3], b = [4, 5, 6]
Output: [1, 4, 2, 5, 3, 6]

Example 2:

Input: a = [1, 2, 3], b = [4, 5]
Output: [1, 4, 2, 5, 3]

Example 3:

Input: a = [1], b = []
Output: [1]

Constraints:

    1 <= number of nodes in a <= 5 * 10**4
    number of nodes in b is len(a) or len(a) - 1
    1 <= Node.val <= 1000

    REQUIRED: O(n) time, O(1) extra space, relink in place. NO new nodes,
    NO list of values.

---

Learning

"""


class Solution:
    def interleave(self, a: ListNode, b: Optional[ListNode]) -> ListNode:
        head = a
        while b:
            a.next, b.next, a, b = b, a.next, a.next, b.next
        return head


sol = Solution()

a = build_linked_list([1, 2, 3])
b = build_linked_list([4, 5])
draw_linked_list(a)
draw_linked_list(b)
print(get_list_values(sol.interleave(a, b)))  # [1, 4, 2, 5, 3]


def weave(x, y):
    return get_list_values(sol.interleave(build_linked_list(x), build_linked_list(y)))


assert weave([1, 2, 3], [4, 5, 6]) == [1, 4, 2, 5, 3, 6]
assert weave([1, 2, 3], [4, 5]) == [1, 4, 2, 5, 3]
assert weave([1], []) == [1]
assert weave([1], [2]) == [1, 2]
assert weave([1, 2], [3]) == [1, 3, 2]
assert weave([1, 2, 3, 4, 5], [9, 8, 7, 6, 5]) == [1, 9, 2, 8, 3, 7, 4, 6, 5, 5]
assert weave(list(range(1, 25001)), list(range(50000, 25000, -1))) == [
    v for i in range(1, 25001) for v in (i, 50001 - i)
]
