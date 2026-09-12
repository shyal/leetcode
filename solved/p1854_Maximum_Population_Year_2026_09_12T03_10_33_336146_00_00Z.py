"""
URL: https://leetcode.com/problems/maximum-population-year/description/?envType=problem-list-v2&envId=vn57k9wr

1854. Maximum Population Year

You are given a 2D integer array logs where each logs[i] = [birth_i, death_i] indicates the birth and death years of the iᵗʰ person.

The population of some year x is the number of people alive during that year. The iᵗʰ person is counted in year x's population if x is in the inclusive range [birth_i, death_i - 1]. Note that the person is not counted in the year that they die.

Return the earliest year with the maximum population.

Example 1:

Input: logs = [[1993,1999],[2000,2010]]
Output: 1993
Explanation: The maximum population is 1, and 1993 is the earliest year with this population.

Example 2:

Input: logs = [[1950,1961],[1960,1971],[1970,1981]]
Output: 1960
Explanation:
The maximum population is 2, and it had happened in years 1960 and 1970.
The earlier year between them is 1960.

Constraints:

    1 <= logs.length <= 100
    1950 <= birth_i < death_i <= 2050
"""


class Solution:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        n = 2050 - 1950 + 1
        buckets = [0] * 3000

        for birth, death in logs:
            buckets[birth] += 1
            buckets[death] -= 1

        max_pop = 0
        best_year = 0
        for i, v in enumerate(accumulate(buckets)):
            if v > max_pop:
                max_pop = v
                best_year = i

        return best_year


sol = Solution()

# print(sol.maximumPopulation([[1993, 1999], [2000, 2010]]))  # 1993

assert sol.maximumPopulation([[1993, 1999], [2000, 2010]]) == 1993
assert sol.maximumPopulation([[1950, 1961], [1960, 1971], [1970, 1981]]) == 1960

assert sol.maximumPopulation([[1950, 1951]]) == 1950
assert sol.maximumPopulation([[1950, 2050]]) == 1950
assert sol.maximumPopulation([[1950, 1952], [1951, 1953], [1952, 1954]]) == 1951
assert sol.maximumPopulation([[2000, 2010], [2000, 2010], [2000, 2010]]) == 2000
assert sol.maximumPopulation([[1999, 2000], [2000, 2001], [2001, 2002]]) == 1999
assert sol.maximumPopulation([[2050, 2051]]) == 2050
assert (
    sol.maximumPopulation(
        [
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
            [1950, 1951],
        ]
    )
    == 1950
)
assert (
    sol.maximumPopulation(
        [
            [1950, 1960],
            [1960, 1970],
            [1970, 1980],
            [1980, 1990],
            [1990, 2000],
            [2000, 2010],
            [2010, 2020],
            [2020, 2030],
            [2030, 2040],
            [2040, 2050],
        ]
    )
    == 1950
)
assert (
    sol.maximumPopulation(
        [
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
            [1950, 2050],
        ]
    )
    == 1950
)
assert (
    sol.maximumPopulation(
        [[1950, 1955], [1951, 1956], [1952, 1957], [1953, 1958], [1954, 1959]]
    )
    == 1954
)
assert sol.maximumPopulation([[2049, 2050]]) == 2049
assert (
    sol.maximumPopulation(
        [
            [1950, 1951],
            [1951, 1952],
            [1952, 1953],
            [1953, 1954],
            [1954, 1955],
            [1955, 1956],
            [1956, 1957],
            [1957, 1958],
            [1958, 1959],
            [1959, 1960],
        ]
    )
    == 1950
)
