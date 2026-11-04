"""
Write a class Reverse that iterates over a sequence `data` from its last
element to its first, and a method `reverse` that returns Reverse(data).
A for loop over it yields the elements backwards, once.

Example 1:

Input: data = "spam"
Output: the iteration yields "m", "a", "p", "s"

Example 2:

Input: data = [1, 2, 3]
Output: the iteration yields 3, 2, 1

Example 3:

Input: data = ""
Output: the iteration yields nothing

Constraints:

    0 <= len(data) <= 10^5

    REQUIRED: Reverse has an index, __iter__ returns self, and
    __next__ returns the next element or raises StopIteration when the
    index reaches 0. NO reversed(), NO slicing, NO yield, NO copy of
    data.
"""


class Reverse:
    def __init__(self, data):
        self.data = data
        self.i = len(data) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= 0:
            res = self.data[self.i]
            self.i -= 1
            return res
        else:
            raise StopIteration()


class Solution:

    def reverse(self, data) -> Reverse:
        return Reverse(data)


sol = Solution()

print(list(sol.reverse("spam")))  # ['m', 'a', 'p', 's']

assert list(sol.reverse("spam")) == ["m", "a", "p", "s"]
assert list(sol.reverse([1, 2, 3])) == [3, 2, 1]
assert list(sol.reverse("")) == []
assert next(sol.reverse("ab")) == "b"
assert iter(sol.reverse("ab")).__class__ is Reverse
it = sol.reverse("x")
assert list(it) == ["x"] and list(it) == []
