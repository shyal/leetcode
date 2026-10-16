"""
URL: https://leetcode.com/problems/peeking-iterator/description/?envType=problem-list-v2&envId=vn57k9wr

284. Peeking Iterator

Design an iterator that supports the peek operation on an existing iterator in addition to the hasNext and the next operations.

Implement the PeekingIterator class:

- PeekingIterator(Iterator<int> nums) Initializes the object with the given integer iterator iterator.
- int next() Returns the next element in the array and moves the pointer to the next element.
- boolean hasNext() Returns true if there are still elements in the array.
- int peek() Returns the next element in the array without moving the pointer.

Note: Each language may have a different implementation of the constructor and Iterator, but they all support the int next() and boolean hasNext() functions.

Example 1:

Input
["PeekingIterator", "next", "peek", "next", "next", "hasNext"]
[[[1, 2, 3]], [], [], [], [], []]
Output
[null, 1, 2, 2, 3, false]

Explanation
PeekingIterator peekingIterator = new PeekingIterator([1, 2, 3]); // [1,2,3]
peekingIterator.next();    // return 1, the pointer moves to the next element [1,2,3].
peekingIterator.peek();    // return 2, the pointer does not move [1,2,3].
peekingIterator.next();    // return 2, the pointer moves to the next element [1,2,3]
peekingIterator.next();    // return 3, the pointer moves to the next element [1,2,3]
peekingIterator.hasNext(); // return False

Constraints:

    1 <= nums.length <= 1000
    1 <= nums[i] <= 1000
    All the calls to next and peek are valid.
    At most 1000 calls will be made to next, hasNext, and peek.

Follow up: How would you extend your design to be generic and work with all types, not just integer?

---

LEETCODE: Accepted (49 ms, 19.5 MB)
"""


# mu 0.12
# class Iterator
#   def __init__(nums)
#     '\n        Initializes an iterator object to the beginning of a list.\n        :type nums: List[int]\n        '
#     self.nums = nums
#     self.it = 0
#
#   def hasNext()
#     self.it <= (len(self.nums) - 1)
#
#   def next()
#     ret res = self.nums[self.it]
#     self.it += 1
#
# class PeekingIterator
#   def __init__(iterator)
#     self.it = iterator
#
#   def peek()
#     '\n        Returns the next element in the iteration without advancing the iterator.\n        :rtype: int\n        '
#     if self.it.hasNext()
#       return self.it.nums[self.it.it]
#
#   def next()
#     '\n        :rtype: int\n        '
#     self.it.next()
#
#   def hasNext()
#     '\n        :rtype: bool\n        '
#     self.it.hasNext()

# mu 0.12
# class Iterator
#   def __init__(nums)
#     self.nums = nums
#     self.it = 0
#
#   def hasNext()
#     self.it <= (len(self.nums) - 1)
#
#   def next()
#     ret res = self.nums[self.it]
#     self.it += 1
#
# class PeekingIterator
#   def __init__(iterator)
#     self.it = iterator
#     self.peeked = None
#
#   def peek()
#     if self.peeked is not None
#       return self.peeked
#     if self.it.hasNext()
#       self.peeked = self.it.next()
#       return self.peeked
#
#   def next()
#     if self.peeked is not None
#       res = self.peeked
#       self.peeked = None
#       return res
#     self.it.next()
#
#   def hasNext()
#     if self.peeked is not None
#       return True
#     self.it.hasNext()

class Iterator:
    def __init__(self, nums):
        self.nums = nums
        self.it = 0

    def hasNext(self):
        return self.it <= (len(self.nums) - 1)

    def next(self):
        res = self.nums[self.it]
        self.it += 1
        return res


class PeekingIterator:
    def __init__(self, iterator):
        self.it = iterator
        self.peeked = None

    def peek(self):
        if self.peeked is not None:
            return self.peeked
        if self.it.hasNext():
            self.peeked = self.it.next()
            return self.peeked

    def next(self):
        if self.peeked is not None:
            res = self.peeked
            self.peeked = None
            return res
        return self.it.next()

    def hasNext(self):
        if self.peeked is not None:
            return True
        return self.it.hasNext()


sol = PeekingIterator(Iterator([1, 2, 3]))
print(sol.next())
print(sol.peek())
print(sol.next())
print(sol.next())
print(sol.hasNext())
_l, _r = PeekingIterator(Iterator([1, 2, 3])).next(), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
iter1 = PeekingIterator(Iterator([1, 2, 3]))
_l, _r = iter1.next(), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = iter1.peek(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = iter1.next(), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = iter1.next(), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = iter1.hasNext(), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = PeekingIterator(Iterator([])).hasNext(), False
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = PeekingIterator(Iterator([5])).peek(), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = PeekingIterator(Iterator([5])).next(), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = PeekingIterator(Iterator([5])).hasNext(), True
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = PeekingIterator(Iterator([-1, -2, -3])).peek(), -1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = PeekingIterator(Iterator([1000] * 1000)).peek(), 1000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
