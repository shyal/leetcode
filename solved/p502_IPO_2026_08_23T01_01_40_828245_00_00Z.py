"""
URL: https://leetcode.com/problems/ipo/description/?envType=problem-list-v2&envId=vn57k9wr

502. IPO

Suppose LeetCode will start its IPO soon. In order to sell a good price of its shares to Venture Capital, LeetCode would like to work on some projects to increase its capital before the IPO. Since it has limited resources, it can only finish at most k distinct projects before the IPO. Help LeetCode design the best way to maximize its total capital after finishing at most k distinct projects.

You are given n projects where the ith project has a pure profit profits[i] and a minimum capital of capital[i] is needed to start it.

Initially, you have w capital. When you finish a project, you will obtain its pure profit and the profit will be added to your total capital.

Pick a list of at most k distinct projects from given projects to maximize your final capital, and return the final maximized capital.

The answer is guaranteed to fit in a 32-bit signed integer.

Example 1:

Input: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
Output: 4
Explanation: Since your initial capital is 0, you can only start the project indexed 0.
After finishing it you will obtain profit 1 and your capital becomes 1.
With capital 1, you can either start the project indexed 1 or the project indexed 2.
Since you can choose at most 2 projects, you need to finish the project indexed 2 to get the maximum capital.
Therefore, output the final maximized capital, which is 0 + 1 + 3 = 4.

Example 2:

Input: k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]
Output: 6

Constraints:

    1 <= k <= 10^5
    0 <= w <= 10^9
    n == profits.length
    n == capital.length
    1 <= n <= 10^5
    0 <= profits[i] <= 10^4
    0 <= capital[i] <= 10^9

---

This looks like a greedy problem. The tricky part is repeatedly searching
the arrays for projects we can afford to work on with max profit.

This suggests a brute force greedy approach at first, followed by an
optimization pass.

If greedy Doesn't work, it becomes a knapsack problem.

Ok i'm pretty shocked this passed all the tests... so either the asserts
are not comprehensive, or this is correct and just needs an optimization pass.

Right now, it's worse case n^2 which won't play well with k being 10^5.

So the greedy solution wasn't the hard part. The hard part is optimizing the
brute force version of this algo.

The obvious thing to do is to reduce the search space.

I'm considering binary search and a heap.

With a max heap keyed by profit, it doesn't really help in case we have lots of
high profit projects above budget.

With a min help keyed by budget, it doesn't help if there are lots of low profit
affordable projects.

If we sort profits and capital by capital, we can quickly isolate the affordable
projects. This reduces the search space at worst case O(log n), so O(n log n) total.

Once that's done, i can just pick the max profit project within that search space.
I can search linearly at first, then do another optimization pass, i.e with the
data sorted by profits instead of capital.

Ok a binary search would work fine, but then the problem because eviction of the
done projecst, which makes bs unsuitable for the task. Mind you.. i could just
keep a done set, and the binary search can't pick the project if its in the done
set.

Before premature optimization, let me confirm the bf solution gets a TLE.

TLE confirmed.

OK I'm going to stop here. I got the greedy approach quickly, and need more
foundations, like building multi-dim binary searches etc. (or whatever)
the non-TLE version of this is.

"""


class Solution:
    def findMaximizedCapital(
        self, k: int, w: int, profits: List[int], capital: List[int]
    ) -> int:

        # sorted_by_cap = [[c, p] for c, p in zip(capital, profits)]
        # sorted_by_cap.sort(key=lambda x: x[0])

        # sorted_by_profit = [[c, p] for c, p in zip(capital, profits)]
        # sorted_by_profit.sort(key=lambda x: x[1])

        done = set([])

        def get_max_profit_project():
            # ind = bisect_right(sorted_by_cap, w, key=lambda x: x[0])
            # print("bisect", ind)
            max_profit = 0
            max_profit_index = -1

            for i, profit in enumerate(profits):
                if i not in done and profit > max_profit and capital[i] <= w:
                    max_profit = profit
                    max_profit_index = i
            return max_profit_index

        for _ in range(k):
            mpi = get_max_profit_project()
            if mpi != -1:
                w += profits[mpi]
                done.add(mpi)
            else:
                break

        return w


sol = Solution()

print(sol.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]))  # 4

assert sol.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
assert sol.findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]) == 6

assert sol.findMaximizedCapital(1, 0, [0], [0]) == 0
assert sol.findMaximizedCapital(1, 0, [1], [1]) == 0
assert sol.findMaximizedCapital(3, 0, [1, 1, 1], [0, 0, 0]) == 3
assert sol.findMaximizedCapital(3, 0, [1, 2, 3], [1, 1, 1]) == 0
assert sol.findMaximizedCapital(3, 10**9, [10**4] * 10, [0] * 10) == 1000030000
assert sol.findMaximizedCapital(0, 0, [1, 2, 3], [0, 1, 1]) == 0
assert sol.findMaximizedCapital(5, 0, [1, 2, 3, 4, 5], [0, 0, 0, 0, 0]) == 15
assert sol.findMaximizedCapital(2, 1, [1, 2, 3], [2, 2, 2]) == 1
assert sol.findMaximizedCapital(2, 0, [0, 0, 0], [0, 0, 0]) == 0
assert sol.findMaximizedCapital(3, 0, [5, 4, 3, 2, 1], [0, 0, 0, 0, 0]) == 12
assert sol.findMaximizedCapital(3, 0, [1, 2, 3], [0, 0, 0]) == 6
assert sol.findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 10**9]) == 3
