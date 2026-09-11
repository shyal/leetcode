r"""
DRILL: Claim Or Merge

Given countries, where countries[i] is the list of border ids of country
i, return the dict owner mapping each border id to the first country
that lists it. Solution extends UnionFind from dsa/union_find.py, built
over the countries. Call self.union on every two countries that share a
border, and never on borders.

Example 1:

Input: countries = [[41, 42], [43], [42, 44], [45, 43]]
Output: {41: 0, 42: 0, 43: 1, 44: 2, 45: 3}
Explanation: border 42 lies between countries 0 and 2, and border 43
between countries 1 and 3. Country 0 is the first to list 42, country 1
the first to list 43.

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

Input: countries = [[47], [47], [47]]
Output: {47: 0}
Explanation: all three countries share border 47.

Example 3:

Input: countries = [[41, 42], [43, 44], [42, 43]]
Output: {41: 0, 42: 0, 43: 1, 44: 1}
Explanation: country 0 and country 1 share no border. Both share one
with country 2.

  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  ______________  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
  ~ ~ ~ ~ ~  ______ /              \______  ~ ~ ~ ~ ~ ~ ~ ~ ~
 ~ ~ ~ ~   _/      \                      \_____  ~ ~ ~ ~ ~ ~
  ~ ~ ~   /         \     country 2             \  ~ ~ ~ ~ ~
 ~ ~ ~   |  country  42                          43   ~ ~ ~ ~
  ~ ~ ~  |     0     /                            \ country  ~
 ~ ~ ~    \    41   /       _______________        |    1    ~
  ~ ~ ~    \_______/       /               \_____  \      44 ~
 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~/ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  \__\_______/
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

Constraints:

    1 <= len(countries) <= 1000
    1 <= len(countries[i]) <= 10
    0 <= border id < 10^6

    REQUIRED: must run in O(L) union and dict operations, where L is the
    total number of border entries. NO country-to-country pair tests; NO
    second pass over countries.

---

Hmm solved it from memory, but need better insight.


"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def claimOrMerge(self, countries: List[List[int]]) -> Dict[int, int]:
        owner = defaultdict(list)
        for i, country in enumerate(countries):
            for border in country:
                if border not in owner:
                    owner[border] = i
                else:
                    self.union(i, owner[border])
                    print("union")
            draw_graphviz(owner)
            print("-----------")
        return owner


sol = Solution(4)

print(
    sol.claimOrMerge([[41, 42], [43], [42, 44], [45, 43]])
)  # {41: 0, 42: 0, 43: 1, 44: 2, 45: 3}

# assert Solution(4).claimOrMerge([[41, 42], [43], [42, 44], [45, 43]]) == {41: 0, 42: 0, 43: 1, 44: 2, 45: 3}
# assert Solution(3).claimOrMerge([[47], [47], [47]]) == {47: 0}
# assert Solution(1).claimOrMerge([[48]]) == {48: 0}
# assert Solution(2).claimOrMerge([[41, 42], [43, 44]]) == {41: 0, 42: 0, 43: 1, 44: 1}
# assert Solution(3).claimOrMerge([[41, 42], [43, 44], [42, 43]]) == {41: 0, 42: 0, 43: 1, 44: 1}
