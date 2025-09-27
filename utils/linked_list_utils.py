from rich import print


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_linked_list(vals):
    dummy = ListNode()
    it = dummy
    for v in vals:
        it.next = ListNode(v)
        it = it.next
    return dummy.next


def print_linked_list(head):
    while head:
        print(head.val, end=(" -> " if head.next else ""))
        head = head.next
    print("")


def get_list_values(head):
    ret = []
    while head:
        ret.append(head.val)
        head = head.next
    return ret
