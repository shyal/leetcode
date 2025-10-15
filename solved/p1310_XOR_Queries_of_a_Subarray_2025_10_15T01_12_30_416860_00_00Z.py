"""
URL: https://leetcode.com/problems/xor-queries-of-a-subarray/description/

1310. XOR Queries of a Subarray

You are given an array arr of positive integers. You are also given the array queries where queries[i] = [lefti, righti].

For each query i compute the XOR of elements from lefti to righti (that is, arr[lefti] XOR arr[lefti + 1] XOR ... XOR arr[righti] ).

Return an array answer where answer[i] is the answer to the ith query.


Example 1:

Input: arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]
Output: [2,7,14,8]
Explanation:
The binary representation of the elements in the array are:
1 = 0001
3 = 0011
4 = 0100
8 = 1000
The XOR values for queries are:
[0,1] = 1 xor 3 = 2
[1,2] = 3 xor 4 = 7
[0,3] = 1 xor 3 xor 4 xor 8 = 14
[3,3] = 8

Example 2:

Input: arr = [4,8,2,10], queries = [[2,3],[1,3],[0,0],[0,3]]
Output: [8,0,4,4]


Constraints:

        1 <= arr.length, queries.length <= 3 * 104
        1 <= arr[i] <= 109
        queries[i].length == 2
        0 <= lefti <= righti < arr.length

---

This seems like a prefix computation of the xors.. so rather than recomputing
the xors within a range each time, they can be precomputed.

I'll do it the brute force way first, so i can compare.

Alright so brute force was easy. Now if we think of the prefix approach,
with simple data: 1, 2, 3

In binary that's

1, 10, 101

let's compute the range: 1, [10, 101]

2 ^ 3 is 1, so we're effectively trying to compute 1, [1]

Now if we accumulate the xors, we get:

1, 11, 0

Which i'm guessing is:

prefix[j] ^ prefix[i-1]

"""


class Solution:

    def get_xor_range(self, i, j, arr):
        return reduce(xor, arr[i : j + 1])

    def xorQueriesBruteForce(
        self, arr: List[int], queries: List[List[int]]
    ) -> List[int]:
        return [self.get_xor_range(i, j, arr) for i, j in queries]

    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        prefix = [*accumulate(arr, func=xor)] + [0]

        def get_range(i, j):
            return prefix[j] ^ prefix[i - 1]

        return [get_range(i, j) for i, j in queries]


sol = Solution()

assert sol.xorQueriesBruteForce(
    arr=[1, 3, 4, 8], queries=[[0, 1], [1, 2], [0, 3], [3, 3]]
) == [2, 7, 14, 8]


assert sol.xorQueries(arr=[1, 3, 4, 8], queries=[[0, 1], [1, 2], [0, 3], [3, 3]]) == [
    2,
    7,
    14,
    8,
]


assert sol.xorQueriesBruteForce(
    arr=[4, 8, 2, 10], queries=[[2, 3], [1, 3], [0, 0], [0, 3]]
) == [
    8,
    0,
    4,
    4,
]

assert sol.xorQueries(arr=[4, 8, 2, 10], queries=[[2, 3], [1, 3], [0, 0], [0, 3]]) == [
    8,
    0,
    4,
    4,
]
