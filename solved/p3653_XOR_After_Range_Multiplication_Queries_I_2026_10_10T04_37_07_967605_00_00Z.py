"""
URL: https://leetcode.com/problems/xor-after-range-multiplication-queries-i/description/?envType=problem-list-v2&envId=vn57k9wr

3653. XOR After Range Multiplication Queries I

You are given an integer array nums of length n and a 2D integer array queries of size q, where queries[i] = [l_i, r_i, k_i, v_i].

For each query, you must apply the following operations in order:

- Set idx = l_i.
- While idx <= r_i:
    - Update: nums[idx] = (nums[idx] * v_i) % (10^9 + 7)
    - Set idx += k_i.

Return the bitwise XOR of all elements in nums after processing all queries.

Example 1:

Input: nums = [1,1,1], queries = [[0,2,1,4]]
Output: 4
Explanation:
A single query [0, 2, 1, 4] multiplies every element from index 0 through index 2 by 4.
The array changes from [1, 1, 1] to [4, 4, 4].
The XOR of all elements is 4 ^ 4 ^ 4 = 4.

Example 2:

Input: nums = [2,3,1,5,4], queries = [[1,4,2,3],[0,2,1,2]]
Output: 31
Explanation:
The first query [1, 4, 2, 3] multiplies the elements at indices 1 and 3 by 3, transforming the array to [2, 9, 1, 15, 4].
The second query [0, 2, 1, 2] multiplies the elements at indices 0, 1, and 2 by 2, resulting in [4, 18, 2, 15, 4].
Finally, the XOR of all elements is 4 ^ 18 ^ 2 ^ 15 ^ 4 = 31.

Constraints:

    1 <= n == nums.length <= 10^3
    1 <= nums[i] <= 10^9
    1 <= q == queries.length <= 10^3
    queries[i] = [l_i, r_i, k_i, v_i]
    0 <= l_i <= r_i < n
    1 <= k_i <= n
    1 <= v_i <= 10^5

---

LEETCODE: Accepted (1669 ms, 20.2 MB)
"""

MOD = 10**9 + 7


# mu 0.7
# def xorAfterQueries(nums: [int], queries: [[int]]) -> int
#   for (l_i, r_i, k_i, v_i) in queries
#     idx = l_i
#     while idx <= r_i
#       nums[idx] = (nums[idx] * v_i) % (10**9 + 7)
#       idx += k_i
#   reduce(xor, nums)

class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def xorAfterQueries(self, nums: list[int], queries: list[list[int]]) -> int:
        _in_queries, queries = queries, Grid(queries)
        _w_queries = queries
        try:
            for (l_i, r_i, k_i, v_i) in queries:
                idx = l_i
                while idx <= r_i:
                    nums[idx] = (nums[idx] * v_i) % (10 ** 9 + 7)
                    idx += k_i
            return reduce(xor, nums)
        finally:
            _in_queries[:] = _w_queries


sol = Solution()
print(sol.xorAfterQueries([1, 1, 1], [[0, 2, 1, 4]]))
_l, _r = sol.xorAfterQueries([1, 1, 1], [[0, 2, 1, 4]]), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([2, 3, 1, 5, 4], [[1, 4, 2, 3], [0, 2, 1, 2]]), 31
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([0], [[0, 0, 1, 1]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([10 ** 9], [[0, 0, 1, 10 ** 5]]), 999300007
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1] * 1000, [[0, 999, 1, 2]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1] * 1000, [[0, 999, 1000, 2]]), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1, 2, 3, 4, 5], [[0, 4, 2, 0]]), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1, 2, 3, 4, 5], [[0, 4, 2, 1]]), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1, 2, 3, 4, 5], [[0, 4, 2, 10 ** 5]]), 177254
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1] * 1000, [[0, 999, 1, 2], [0, 999, 2, 3], [0, 999, 3, 4]]), 20
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([10 ** 9] * 1000, [[0, 999, 1, 10 ** 5]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1] * 10, [[0, 9, 1, 2], [0, 9, 1, 3], [0, 9, 1, 4], [0, 9, 1, 5]]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1] * 5, [[0, 4, 1, 2], [1, 3, 1, 3], [2, 2, 1, 4]]), 24
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.xorAfterQueries([1, 1, 1, 1, 1], [[0, 4, 1, 2], [0, 4, 1, 2], [0, 4, 1, 2]]), 8
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
