"""
EPI 8.1 Implement a stack with max API

Implement a stack of integers. Solution() makes an empty stack with
these methods:

    push(x)   puts x on top and returns nothing
    pop()     removes the top value and returns it
    max()     returns the largest value in the stack
    empty()   returns True when the stack holds no values

The methods pop() and max() are called only on a stack that is not
empty.

Example 1:

    st = Solution()
    st.push(2)
    st.push(5)
    st.push(1)
    st.max()     -> 5
    st.pop()     -> 1
    st.pop()     -> 5
    st.max()     -> 2
    st.empty()   -> False

Example 2:

    st = Solution()
    st.push(3)
    st.push(3)
    st.pop()     -> 3
    st.max()     -> 3     (the other 3 is still in the stack)

Constraints:

    -10^9 <= x <= 10^9
    up to 3 * 10^5 calls

    REQUIRED: O(1) time per call. NO max() over the stored values, NO
    heap, NO sort.
"""


class Solution:
    def empty(self) -> bool:
        pass

    def max(self) -> int:
        pass

    def pop(self) -> int:
        pass

    def push(self, x: int) -> None:
        pass


sol = Solution()

sol.push(2)
sol.push(5)
sol.push(1)
print(sol.max())  # 5

# sol = Solution()
# assert sol.empty() is True
# sol.push(2)
# sol.push(5)
# sol.push(1)
# assert sol.max() == 5
# assert sol.pop() == 1
# assert sol.max() == 5
# assert sol.pop() == 5
# assert sol.max() == 2
# assert sol.empty() is False
# assert sol.pop() == 2
# assert sol.empty() is True
# sol.push(3)
# sol.push(3)
# assert sol.pop() == 3 and sol.max() == 3
# sol.push(-7)
# assert sol.max() == 3
# assert sol.pop() == -7 and sol.pop() == 3 and sol.empty() is True
# sol.push(-7)
# assert sol.max() == -7
# _ = [sol.push(x) for x in range(100000)]
# assert all(sol.max() == 99999 for _ in range(100000))
# assert [sol.pop() for _ in range(3)] == [99999, 99998, 99997] and sol.max() == 99996
# assert all(sol.max() == x and sol.pop() == x for x in range(99996, -1, -1))
# assert sol.max() == -7 and sol.pop() == -7 and sol.empty() is True
