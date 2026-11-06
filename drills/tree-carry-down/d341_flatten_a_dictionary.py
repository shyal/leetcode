"""
Given a dictionary whose values are strings or dictionaries of the same
kind, return a flat dictionary from paths to strings. The path of a
string is the keys on the way down to it joined with '.'. An empty key
adds nothing to the path, not even a dot.

Example 1:

Input: dictionary = {"Key1": "1",
                     "Key2": {"a": "2", "b": "3",
                              "c": {"d": "3", "e": {"": "1"}}}}
Output: {"Key1": "1", "Key2.a": "2", "Key2.b": "3",
         "Key2.c.d": "3", "Key2.c.e": "1"}
Explanation: the string "1" under e sits under the empty key, so its
path is "Key2.c.e", not "Key2.c.e.".

Example 2:

Input: dictionary = {"": {"a": "1"}, "b": "3"}
Output: {"a": "1", "b": "3"}
Explanation: the empty key at the top adds nothing, so the path of "1"
is "a".

Example 3:

Input: dictionary = {"a": "1"}
Output: {"a": "1"}

Constraints:

    0 <= number of keys in total <= 10^4
    Keys are strings. Values are strings or dictionaries.
    The paths of the strings are distinct.
    Nesting depth <= 100

    REQUIRED: O(n) time, where n is the total number of keys. NO
    repr(), NO json, NO string parsing.
"""


class Solution:
    def flatten_dictionary(self, dictionary: dict) -> dict:
        pass


sol = Solution()

print(sol.flatten_dictionary({"Key1": "1", "Key2": {"a": "2", "b": "3", "c": {"d": "3", "e": {"": "1"}}}}))  # {'Key1': '1', 'Key2.a': '2', 'Key2.b': '3', 'Key2.c.d': '3', 'Key2.c.e': '1'}

# assert sol.flatten_dictionary({"Key1": "1", "Key2": {"a": "2", "b": "3", "c": {"d": "3", "e": {"": "1"}}}}) == {"Key1": "1", "Key2.a": "2", "Key2.b": "3", "Key2.c.d": "3", "Key2.c.e": "1"}
# assert sol.flatten_dictionary({"": {"a": "1"}, "b": "3"}) == {"a": "1", "b": "3"}
# assert sol.flatten_dictionary({"a": "1"}) == {"a": "1"}
# assert sol.flatten_dictionary({"Key1": "1", "Key2": {"a": "2", "b": "3", "c": {"d": "3", "e": "1"}}}) == {"Key1": "1", "Key2.a": "2", "Key2.b": "3", "Key2.c.d": "3", "Key2.c.e": "1"}
# assert sol.flatten_dictionary({"Key": {"a": "2", "b": "3"}}) == {"Key.a": "2", "Key.b": "3"}
# assert sol.flatten_dictionary({"Key1": "1", "Key2": {"a": "2", "b": "3", "c": {"d": "3", "e": {"f": "4"}}}}) == {"Key1": "1", "Key2.a": "2", "Key2.b": "3", "Key2.c.d": "3", "Key2.c.e.f": "4"}
# assert sol.flatten_dictionary({"a": {"b": {"c": {"d": {"e": {"f": {"": "awesome"}}}}}}}) == {"a.b.c.d.e.f": "awesome"}
# assert sol.flatten_dictionary({}) == {}
# assert sol.flatten_dictionary({"a": {}}) == {}
# assert sol.flatten_dictionary({"": "x"}) == {"": "x"}
# assert sol.flatten_dictionary({"a": {"": {"": "x"}}}) == {"a": "x"}
# deep = reduce(lambda d, k: {"k": d}, range(100), "x")
# assert sol.flatten_dictionary(deep) == {".".join(["k"] * 100): "x"}
# wide = {str(i): {"v": str(i)} for i in range(5000)}
# assert sol.flatten_dictionary(wide) == {f"{i}.v": str(i) for i in range(5000)}
