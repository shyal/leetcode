"""
DRILL: Swap First Two

Given the head of a linked list, swap the first two nodes and return the
new head. A list with fewer than two nodes is returned unchanged. The
nodes move; their val fields do not.

Example 1:

Input: head = [1, 2, 3, 4]
Output: [2, 1, 3, 4]

Example 2:

Input: head = [1, 2]
Output: [2, 1]

Example 3:

Input: head = [1]
Output: [1]

Constraints:

    0 <= number of nodes <= 100
    0 <= Node.val <= 100

    REQUIRED: O(1) extra space, relink the two nodes in place. NO copying
    nodes into a list, NO writing to val.
"""


# mu 0.12
# class Solution
#   def swapFirstTwo(head: ListNode?) -> ListNode?
#     if not head or not head.next
#       return head
#     ret res = head.next
#     head.next.next, head.next = head, head.next.next

from typing import Optional


class Solution:
    def swapFirstTwo(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        res = head.next
        head.next.next, head.next = head, head.next.next
        return res


sol = Solution()
head = build_linked_list([1, 2, 3, 4])
draw_linked_list(head)
print(get_list_values(sol.swapFirstTwo(head)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list([1, 2, 3, 4]))), [2, 1, 3, 4]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list([1, 2]))), [2, 1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list([1]))), [1]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list([]))), []
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list([1, 2, 3]))), [2, 1, 3]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list([5, 5, 5]))), [5, 5, 5]
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = get_list_values(sol.swapFirstTwo(build_linked_list(list(range(0, 100))))), [1, 0] + list(range(2, 100))
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
