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

---

Passes here, but fails tests on leetcode. This is clearly a horribly bruteforce solution.

"""


class Solution:
    def maximumPopulation(self, logs: List[List[int]]) -> int:
        populations = defaultdict(int)
        for birth, death in logs:
            for b, d in logs:
                if b <= birth and d > birth:
                    populations[birth] += 1
        pop_years = defaultdict(list)

        for year, population in populations.items():
            pop_years[population].append(year)

        print(pop_years)

        max_pop_years = next(iter(sorted(pop_years, reverse=True)))
        return next(iter(sorted(pop_years[max_pop_years])))


sol = Solution()

# print(sol.maximumPopulation([[1993, 1999], [2000, 2010]]))  # 1993
print(
    sol.maximumPopulation(
        [
            [1966, 1968],
            [1954, 2030],
            [1966, 1994],
            [2030, 2044],
            [1988, 2036],
            [1977, 2050],
            [2036, 2046],
            [1989, 2048],
            [2049, 2050],
            [2008, 2019],
            [2022, 2031],
            [1970, 2024],
            [1957, 1996],
            [1991, 2034],
            [1956, 1996],
            [1959, 1969],
            [2021, 2050],
        ]
    )
)  # 1991

assert (
    sol.maximumPopulation(
        [
            [2033, 2034],
            [2039, 2047],
            [1998, 2042],
            [2047, 2048],
            [2025, 2029],
            [2005, 2044],
            [1990, 1992],
            [1952, 1956],
            [1984, 2014],
        ]
    )
    == 2005
)

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


# FAILED: walked away after 24m 51s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
