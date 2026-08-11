# FORCED STYLE — `make solved` will reject this solve unless it uses:
#   • Dict values beyond counts: Store indices, last-seen positions, or mappings as dict values — choose WHAT to remember.
# (`make unforce` drops the constraint)

"""
URL: https://leetcode.com/problems/count-items-matching-a-rule/description/?envType=problem-list-v2&envId=vn57k9wr

1773. Count Items Matching a Rule

You are given an array items, where each items[i] = [type_i, color_i, name_i]
describes the type, color, and name of the ith item. You are also given a rule
represented by two strings, ruleKey and ruleValue.

The ith item is said to match the rule if one of the following is true:

    - ruleKey == "type" and ruleValue == type_i.
    - ruleKey == "color" and ruleValue == color_i.
    - ruleKey == "name" and ruleValue == name_i.

Return the number of items that match the given rule.


Example 1:

Input: items = [["phone","blue","pixel"],["computer","silver","lenovo"],["phone","gold","iphone"]], ruleKey = "color", ruleValue = "silver"
Output: 1
Explanation: There is only one item matching the given rule, which is ["computer","silver","lenovo"].

Example 2:

Input: items = [["phone","blue","pixel"],["computer","silver","phone"],["phone","gold","iphone"]], ruleKey = "type", ruleValue = "phone"
Output: 2
Explanation: There are only two items matching the given rule, which are ["phone","blue","pixel"] and ["phone","gold","iphone"]. Note that the item ["computer","silver","phone"] does not match.


Constraints:

    1 <= items.length <= 10^4
    1 <= type_i.length, color_i.length, name_i.length, ruleValue.length <= 10
    ruleKey is equal to either "type", "color", or "name".
    All strings consist only of lowercase letters.
"""


class Solution:
    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        return sum(dict(type=it[0], color=it[1], name=it[2])[ruleKey] == ruleValue for it in items)

sol = Solution()

assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]],
        "color",
        "silver",
    )
    == 1
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "phone"], ["phone", "gold", "iphone"]],
        "type",
        "phone",
    )
    == 2
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"], ["phone", "gold", "iphone"]],
        "name",
        "iphone",
    )
    == 1
)
assert sol.countMatches([["phone", "blue", "pixel"]], "type", "phone") == 1
assert sol.countMatches([["phone", "blue", "pixel"]], "type", "pixel") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "name", "phone") == 0
assert sol.countMatches([["phone", "blue", "pixel"]], "color", "blue") == 1
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["phone", "gold", "iphone"], ["phone", "red", "nokia"]],
        "type",
        "phone",
    )
    == 3
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["computer", "silver", "lenovo"]],
        "color",
        "green",
    )
    == 0
)
assert (
    sol.countMatches(
        [["blue", "blue", "blue"], ["blue", "red", "green"], ["red", "blue", "green"]],
        "color",
        "blue",
    )
    == 2
)
assert (
    sol.countMatches(
        [["blue", "blue", "blue"], ["blue", "red", "green"], ["red", "blue", "green"]],
        "type",
        "blue",
    )
    == 2
)
assert (
    sol.countMatches(
        [["blue", "blue", "blue"], ["blue", "red", "green"], ["red", "blue", "green"]],
        "name",
        "blue",
    )
    == 1
)
assert (
    sol.countMatches(
        [["phone", "blue", "pixel"], ["phone", "blue", "pixel"]],
        "name",
        "pixel",
    )
    == 2
)
assert sol.countMatches([["a", "b", "c"]], "name", "cc") == 0
assert sol.countMatches([["phone", "blue", "pixel"]] * 100, "type", "phone") == 100