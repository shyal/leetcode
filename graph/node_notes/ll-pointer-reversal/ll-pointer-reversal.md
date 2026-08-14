```python
def reverseSubList(self, head):
    d = ListNode(-1)
    tail = head
    while head:
        # don't hunt him = him don't hunt
        d.next, head.next, head = head, d.next, head.next
    # don't try
    return d.next, tail
```
