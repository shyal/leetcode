# ll_utils.py
#
# Linked list helpers a solution may call, preloaded by sitecustomize. The
# builders and drawers stay in linked_list_utils; this module holds only what
# is sent to leetcode with a submission.

from math import inf
from typing import Optional, Tuple

from Types import ListNode


def linked_list_reverse_k(
    h: Optional[ListNode], k: float = inf
) -> Tuple[Optional[ListNode], Optional[ListNode]]:
    """Reverse the first k nodes of the list at h, in place.

    Returns the new head and the new tail. The tail is the node that was h,
    and its next is the first node that was not reversed. With k left out,
    or a list shorter than k, the whole list is reversed and the tail's next
    is None.

    >>> head, tail = linked_list_reverse_k(build_linked_list([1, 2, 3, 4, 5]), 3)
    >>> get_list_values(head), tail.val
    ([3, 2, 1, 4, 5], 1)
    """
    d = ListNode()
    t = h
    while h and k > 0:
        d.next, h.next, h = h, d.next, h.next
        k -= 1
    if t:
        t.next = h
    return d.next, t
