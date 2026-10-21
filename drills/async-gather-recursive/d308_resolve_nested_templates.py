"""
DRILL: Resolve Nested Templates
TRAINS: async-gather-recursive

The input is a string template and an async function get_data(key: str) -> str.

A placeholder consists of two opening braces, a key string, and two closing braces, written as {{key}}. Replace each placeholder occurrence with the string returned by await get_data(key). Resolve placeholders in each returned string recursively until the result contains no placeholders. Replace every occurrence, including repeated keys. Keep all text outside placeholders unchanged.

Return the fully resolved string. Return a template with no placeholders unchanged.

Implement this method in mu, a Python dialect where self is implicit:

class Solution
  async def mustachify(template: str, get_data) -> str

The tests provide get_data with a fixed table of string keys and string values. For a key in the table, get_data returns the table value immediately. For any other key, it waits with asyncio.sleep(DELAY) and returns "x" + key. DELAY is a fixed positive duration.

Measure total running time in units of DELAY, excluding execution overhead. A dependency path starts at a placeholder in template and follows placeholders in returned values until it reaches a value with no placeholders. The delay count of a path is the number of waits on that path.

Example 1:
Input:
table = {"A": "Alpha", "BB": "{{B1}} and {{B2}}", "C": "{{C1}}, {{C2}}, {{EE}}", "DD": "Delta", "EE": "{{F1}} and {{F2}}"}
template = "A:{{A}}, Y:{{Y}}, B:{{BB}}, Z:{{Z}} C:{{C}} D:{{DD}}."
Output:
A:Alpha, Y:xY, B:xB1 and xB2, Z:xZ C:xC1, xC2, xF1 and xF2 D:Delta.
Explanation: A maps to Alpha; DD maps to Delta; BB maps to xB1 and xB2; C maps to xC1, xC2, xF1 and xF2; Y maps to xY; Z maps to xZ; the total running time is one delay.

Example 2:
Input:
table = {"P": "{{Q}}-{{Q}}", "Q": "{{R}}"}
template = "{{P}}!"
Output:
xR-xR!
Explanation: Each Q maps through R to xR, so P maps to xR-xR; the total running time is one delay.

Example 3:
Input:
table = {}
template = "no keys"
Output:
no keys
Explanation: The template contains no placeholders, so its text stays unchanged and the total running time is zero delays.

Constraints:
The length of template is from 0 to 10^4 characters.
Keys are non-empty strings that contain no braces.
Each table value is a string.
Nesting depth is the number of placeholders on a dependency path; it is at most 50.
The total number of placeholder occurrences across template and all recursively inserted values is at most 10^3, with repeated occurrences counted separately.
The expansion has no cycle.
REQUIRED: Total running time must equal the largest delay count on any dependency path, or zero when there are no placeholders; in Example 1, it must be one delay. NO level-by-level rounds, NO awaiting keys one at a time.
"""

import asyncio
import re
import time

DELAY = 0.05


def lookup(table: dict):
    async def get_data(key: str) -> str:
        if key in table:
            return table[key]
        await asyncio.sleep(DELAY)
        return "x" + key

    return get_data


def delays(template: str, table: dict) -> int:
    start = time.perf_counter()
    asyncio.run(Solution().mustachify(template, lookup(table)))
    return round((time.perf_counter() - start) / DELAY)


class Solution:
    async def mustachify(self, template: str, get_data) -> str:
        pass


sol = Solution()

table = {"A": "Alpha", "BB": "{{B1}} and {{B2}}", "C": "{{C1}}, {{C2}}, {{EE}}", "DD": "Delta", "EE": "{{F1}} and {{F2}}"}
print(table)
template = "A:{{A}}, Y:{{Y}}, B:{{BB}}, Z:{{Z}} C:{{C}} D:{{DD}}."
print(template)
print(asyncio.run(sol.mustachify(template, lookup(table))))  # A:Alpha, Y:xY, B:xB1 and xB2, Z:xZ C:xC1, xC2, xF1 and xF2 D:Delta.

# assert asyncio.run(sol.mustachify(template, lookup(table))) == "A:Alpha, Y:xY, B:xB1 and xB2, Z:xZ C:xC1, xC2, xF1 and xF2 D:Delta."
# assert delays(template, table) == 1
# assert asyncio.run(sol.mustachify("{{P}}!", lookup({"P": "{{Q}}-{{Q}}", "Q": "{{R}}"}))) == "xR-xR!"
# assert delays("{{P}}!", {"P": "{{Q}}-{{Q}}", "Q": "{{R}}"}) == 1
# assert asyncio.run(sol.mustachify("no keys", lookup({}))) == "no keys"
# assert delays("no keys", {}) == 0
# assert asyncio.run(sol.mustachify("", lookup({}))) == ""
# assert asyncio.run(sol.mustachify("{{A}}{{A}}", lookup({"A": "Alpha"}))) == "AlphaAlpha"
# assert delays("{{A}}{{A}}", {"A": "Alpha"}) == 0
# assert asyncio.run(sol.mustachify("{{D1}}", lookup({"D1": "{{s1}} {{D2}}", "D2": "{{s2}} {{D3}}", "D3": "{{s3}}"}))) == "xs1 xs2 xs3"
# assert delays("{{D1}}", {"D1": "{{s1}} {{D2}}", "D2": "{{s2}} {{D3}}", "D3": "{{s3}}"}) == 1
# assert asyncio.run(sol.mustachify("{{K0}}", lookup({f"K{i}": f"<{{{{K{i + 1}}}}}>" for i in range(49)}))) == "<" * 49 + "xK49" + ">" * 49
# assert delays("{{K0}}", {f"K{i}": f"{{{{s{i}}}}}{{{{K{i + 1}}}}}" for i in range(49)}) == 1
# assert delays("".join(f"{{{{k{i}}}}}" for i in range(1000)), {}) == 1
