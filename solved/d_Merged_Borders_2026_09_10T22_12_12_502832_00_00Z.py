r"""
DRILL: Merged Borders

Given countries, where countries[i] is the list of border ids of country
i, return the dict mapping the head of each group of countries to the
set of border ids across the countries of that group. Solution extends
UnionFind from dsa/union_find.py, built over the countries, and
self.parent already groups them: self.find(i) returns the head of the
group country i is in.

Example 1:

Input: parent = [2, 3, 2, 3], countries = [[41, 42], [43], [42, 44], [45, 43]]
Output: {2: {41, 42, 44}, 3: {43, 45}}
Explanation: countries 0 and 2 are in the group headed by 2. Countries 1
and 3 are in the group headed by 3.

  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~   ________________  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
  ~ ~ ~   /                \_________  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~   |  country 0      42          \  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
  ~ ~ ~   \      41        /  country 2 |  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~   \______________/         44  /  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ \____________/  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   __________  ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   ______/          \______  ~ ~ ~ ~ ~
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   /                        \  ~ ~ ~ ~
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   | country 1  43  country 3 |  ~ ~ ~ ~
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   \_________/  \_____   45  /  ~ ~ ~ ~
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   \_____/  ~ ~ ~ ~ ~
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

Example 2:

Input: parent = [1, 2, 2], countries = [[47], [47], [47]]
Output: {2: {47}}

Constraints:

    1 <= len(countries) <= 1000
    1 <= len(countries[i]) <= 10
    0 <= border id < 10^6
    parent is free of cycles

    REQUIRED: must call self.find at most once per country. NO
    country-to-country pair tests; NO scan for heads other than through
    self.find.

---

Learning

"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def mergeBorders(self, countries: List[List[int]]) -> Dict[int, set]:
        groups = defaultdict(set)
        for i, borders in enumerate(countries):
            head = self.find(i)
            for border in borders:
                groups[head].add(border)
        return groups


sol = Solution(4)
sol.parent[0] = 2
sol.parent[1] = 3

print(
    sol.mergeBorders([[41, 42], [43], [42, 44], [45, 43]])
)  # {2: {41, 42, 44}, 3: {43, 45}}

sol = Solution(4)
sol.parent[0] = 2
sol.parent[1] = 3
assert sol.mergeBorders([[41, 42], [43], [42, 44], [45, 43]]) == {
    2: {41, 42, 44},
    3: {43, 45},
}

sol = Solution(3)
sol.parent[0] = 1
sol.parent[1] = 2
assert sol.mergeBorders([[47], [47], [47]]) == {2: {47}}

sol = Solution(1)
assert sol.mergeBorders([[48]]) == {0: {48}}

sol = Solution(2)
assert sol.mergeBorders([[41, 42], [43, 44]]) == {0: {41, 42}, 1: {43, 44}}

sol = Solution(3)
sol.parent[0] = 2
sol.parent[1] = 2
assert sol.mergeBorders([[41, 42], [43, 44], [42, 43]]) == {2: {41, 42, 43, 44}}
