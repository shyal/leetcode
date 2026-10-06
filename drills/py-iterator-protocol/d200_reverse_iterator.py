"""
DRILL: Reverse Iterator
TRAINS: py-iterator-protocol

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

    REQUIRED: Reverse keeps an index, __iter__ returns self, and
    __next__ returns the next element or raises StopIteration when the
    index reaches 0. NO reversed(), NO slicing, NO yield, NO copy of
    data.
"""


class Reverse:
    pass


class Solution:

    def reverse(self, data) -> Reverse:
        pass


sol = Solution()

print(list(sol.reverse("spam")))  # ['m', 'a', 'p', 's']

# assert list(sol.reverse("spam")) == ["m", "a", "p", "s"]
# assert list(sol.reverse([1, 2, 3])) == [3, 2, 1]
# assert list(sol.reverse("")) == []
# assert next(sol.reverse("ab")) == "b"
# assert iter(sol.reverse("ab")).__class__ is Reverse
# it = sol.reverse("x")
# assert list(it) == ["x"] and list(it) == []
