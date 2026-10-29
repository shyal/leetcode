# Take every pair of positions i < j in xs. The pair counts when
# key(xs[i]) == lookup(xs[j]). The function key gives the key a number is stored
# under, and the function lookup gives the key a number looks for. Return how
# many pairs count.
#
# Example 1:
#
# Input: xs = [3, 1, 4, 6, 3], key = lambda x: x, lookup = lambda x: x - 2
# Output: 2
# Explanation: The 6 looks for 4, and a 4 is earlier. The last 3 looks for
# 1, and a 1 is earlier. The first 3 looks for 1 too, but no 1 is earlier.
#
# Example 2:
#
# Input: xs = [2, 9, 4, 16, 7, 23], key = lambda x: x % 7, lookup = lambda x: x % 7
# Output: 6
# Explanation: 2, 9, 16 and 23 all have key 2. Four numbers make 6 pairs.
#
# Constraints:
#
#     0 <= len(xs) <= 10^5
#     -10^9 <= xs[i] <= 10^9
#     key and lookup each run in O(1).
#
#     REQUIRED: O(n), one pass over xs. NO enumeration of index pairs.
#
# ---

# mu 0.14

class Solution
  def countPairs(xs: [int], key: int -> int, lookup: int -> int) -> int
    D = counter()
    sum for x in xs
      got = D[lookup(x)]
      D[key(x)] += 1
      got


sol = Solution()

print(sol.countPairs([3, 1, 4, 6, 3], x -> x, x -> x - 2))  # 2

assert sol.countPairs([3, 1, 4, 6, 3], x -> x, x -> x - 2) == 2
assert sol.countPairs([2, 9, 4, 16, 7, 23], x -> x % 7, x -> x % 7) == 6
assert sol.countPairs([], x -> x, x -> x) == 0
assert sol.countPairs([5], x -> x, x -> x) == 0
assert sol.countPairs([4, 4], x -> x, x -> x) == 1
assert sol.countPairs([2, 2, 2], x -> x, x -> x) == 3
assert sol.countPairs([1, 3], x -> x, x -> x - 2) == 1
assert sol.countPairs([3, 1], x -> x, x -> x - 2) == 0
assert sol.countPairs([1, 5, 5, 5, 3], x -> x, x -> x - 2) == 1
assert sol.countPairs([1, 4, 5, 9, 10], x -> x % 5, x -> -x % 5) == 3
assert sol.countPairs([7] * 10 ** 5, x -> x, x -> x) == 4999950000
assert sol.countPairs(list(0..<10 ** 5), x -> x, x -> x - 1) == 99999
assert avoids(Solution, count_pairs)
