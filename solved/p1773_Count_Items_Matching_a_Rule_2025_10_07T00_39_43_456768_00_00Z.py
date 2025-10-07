"""
URL: https://leetcode.com/problems/count-items-matching-a-rule/description/

1773. Count Items Matching a Rule

You are given an array items, where each items[i] = [type_i, color_i, name_i] describes the type, color, and name of the i-th item. You are also given a rule represented by two strings, ruleKey and ruleValue.

The i-th item is said to match the rule if one of the following is true:

    ruleKey == "type" and type_i == ruleValue.
    ruleKey == "color" and color_i == ruleValue.
    ruleKey == "name" and name_i == ruleValue.

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


class Rule:
    type = 0
    color = 1
    name = 2


class Solution:
    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        matches = 0
        for item in items:
            rule_one_matches = ruleKey == "type" and ruleValue == item[Rule.type]
            rule_two_matches = ruleKey == "color" and ruleValue == item[Rule.color]
            rule_three_matches = ruleKey == "name" and ruleValue == item[Rule.name]
            if rule_one_matches or rule_two_matches or rule_three_matches:
                matches += 1
        return matches


sol = Solution()

assert (
    sol.countMatches(
        [
            ["phone", "blue", "pixel"],
            ["computer", "silver", "lenovo"],
            ["phone", "gold", "iphone"],
        ],
        "color",
        "silver",
    )
    == 1
)
assert (
    sol.countMatches(
        [
            ["phone", "blue", "pixel"],
            ["computer", "silver", "phone"],
            ["phone", "gold", "iphone"],
        ],
        "type",
        "phone",
    )
    == 2
)
assert sol.countMatches([["phone", "blue", "pixel"]], "type", "phone") == 1
assert sol.countMatches([["phone", "blue", "pixel"]], "type", "computer") == 0
assert (
    sol.countMatches(
        [
            ["phone", "blue", "pixel"],
            ["computer", "silver", "lenovo"],
            ["phone", "gold", "iphone"],
        ],
        "name",
        "lenovo",
    )
    == 1
)
assert (
    sol.countMatches(
        [
            ["phone", "blue", "pixel"],
            ["computer", "silver", "phone"],
            ["phone", "gold", "iphone"],
        ],
        "name",
        "phone",
    )
    == 1
)
assert (
    sol.countMatches([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]], "color", "b")
    == 1
)
assert (
    sol.countMatches([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]], "color", "z")
    == 0
)
assert sol.countMatches([["type", "color", "name"]], "name", "name") == 1
assert (
    sol.countMatches([["abcdefghij", "klmnopqrst", "uvwxyzabcd"]], "type", "abcdefghij")
    == 1
)
assert (
    sol.countMatches(
        [
            ["phone", "blue", "pixel"],
            ["tablet", "blue", "android"],
            ["phone", "red", "iphone"],
        ],
        "color",
        "blue",
    )
    == 2
)
assert (
    sol.countMatches(
        [
            ["phone", "blue", "pixel"],
            ["tablet", "blue", "android"],
            ["phone", "red", "iphone"],
        ],
        "color",
        "green",
    )
    == 0
)
