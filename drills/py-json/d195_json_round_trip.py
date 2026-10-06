"""
DRILL: JSON Round Trip
TRAINS: py-json

Given a value `obj` made of dicts, lists, strings, numbers, booleans and
None, return its JSON text with the keys of every dict in sorted order.
A second method, `decode`, takes JSON text and returns the value back.

Example 1:

Input: obj = [1, "simple", "list"]
Output: '[1, "simple", "list"]'

Example 2:

Input: obj = {"b": 1, "a": [1, "two"]}
Output: '{"a": [1, "two"], "b": 1}'

Example 3:

Input: obj = None
Output: 'null'

Constraints:

    obj nests at most 10 levels deep.
    decode(encode(obj)) == obj for every valid obj.

    REQUIRED: json.dumps with sort_keys for encode and json.loads for
    decode. NO str(), NO repr(), NO eval(), NO hand-built text.
"""

import json


class Solution:

    def encode(self, obj) -> str:
        pass

    def decode(self, text: str):
        pass


sol = Solution()

print(sol.encode({"b": 1, "a": [1, "two"]}))  # {"a": [1, "two"], "b": 1}

# assert sol.encode([1, "simple", "list"]) == '[1, "simple", "list"]'
# assert sol.encode({"b": 1, "a": [1, "two"]}) == '{"a": [1, "two"], "b": 1}'
# assert sol.encode(None) == "null"
# assert sol.encode({"ok": True, "n": 1.5}) == '{"n": 1.5, "ok": true}'
# assert sol.decode('{"a": [1, "two"], "b": 1}') == {"a": [1, "two"], "b": 1}
# assert sol.decode(sol.encode({"x": [None, False, {"y": "z"}]})) == {"x": [None, False, {"y": "z"}]}
