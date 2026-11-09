"""
EPI 5.11 Compute the next permutation

Given a list of integers perm, return the next permutation of perm in
lexicographic order: the smallest order of the same elements that is
larger than perm. Return [] when no order of the elements is larger.

Example 1:

Input: perm = [1, 0, 3, 2]
Output: [1, 2, 0, 3]

Example 2:

Input: perm = [3, 2, 1, 0]
Output: []
Explanation: The elements are in decreasing order, so no order is
larger.

Example 3:

Input: perm = [6, 2, 1, 5, 4, 3, 0]
Output: [6, 2, 3, 0, 1, 4, 5]

Constraints:

    1 <= len(perm) <= 10^5
    0 <= perm[i] <= 10^5
    perm can hold the same value more than once.

    REQUIRED: O(n) time, O(1) extra space besides the list returned.
    NO permutations(), NO sort.
"""


class Solution:
    def next_permutation(self, perm: list[int]) -> list[int]:
        pass


sol = Solution()

print(sol.next_permutation([1, 0, 3, 2]))  # [1, 2, 0, 3]

# assert sol.next_permutation([1, 0, 3, 2]) == [1, 2, 0, 3]
# assert sol.next_permutation([3, 2, 1, 0]) == []
# assert sol.next_permutation([6, 2, 1, 5, 4, 3, 0]) == [6, 2, 3, 0, 1, 4, 5]
# assert sol.next_permutation([1]) == []
# assert sol.next_permutation([0, 1]) == [1, 0]
# assert sol.next_permutation([1, 0]) == []
# assert sol.next_permutation([1, 2, 3]) == [1, 3, 2]
# assert sol.next_permutation([1, 3, 2]) == [2, 1, 3]
# assert sol.next_permutation([2, 3, 1]) == [3, 1, 2]
# assert sol.next_permutation([1, 1, 5]) == [1, 5, 1]
# assert sol.next_permutation([1, 5, 1]) == [5, 1, 1]
# assert sol.next_permutation([5, 1, 1]) == []
# assert sol.next_permutation([2, 2, 0, 4, 3, 1]) == [2, 2, 1, 0, 3, 4]
# assert sol.next_permutation([4, 4, 4]) == []
# assert sol.next_permutation(list(range(10 ** 5))) == list(range(10 ** 5 - 2)) + [10 ** 5 - 1, 10 ** 5 - 2]
# assert sol.next_permutation(list(range(10 ** 5, 0, -1))) == []
# assert sol.next_permutation([0] + list(range(10 ** 5 - 1, 0, -1))) == [1, 0] + list(range(2, 10 ** 5))
