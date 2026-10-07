# combo chain: backend-live-coding, problem 5 of 10. Run `make combos backend-live-coding` to see
# the chain and what is done this lap; the chain is saved in graph/chains/backend-live-coding.json.
"""
URL: https://leetcode.com/problems/time-based-key-value-store/description/?envType=problem-list-v2&envId=vn57k9wr

981. Time Based Key-Value Store

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:

- TimeMap() Initializes the object of the data structure.
- void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.
- String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".

Example 1:

Input
["TimeMap","set","get","get","set","get","get"]
[[],["foo","bar",1],["foo",1],["foo",3],["foo","bar2",4],["foo",4],["foo",5]]
Output
[null,null,"bar","bar",null,"bar2","bar2"]

Explanation
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);         // return "bar"
timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);         // return "bar2"
timeMap.get("foo", 5);         // return "bar2"

Constraints:

    1 <= key.length, value.length <= 100
    key and value consist of lowercase English letters and digits.
    1 <= timestamp <= 10^7
    All the timestamps timestamp of set are strictly increasing.
    At most 2 * 10^5 calls will be made to set and get.

---

LEETCODE: Accepted (8282 ms, 67.7 MB)
"""


class TimeMap:

    def __init__(self):
        self.d = defaultdict(dict)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.d[key][timestamp] = value

    def get(self, key: str, timestamp: int) -> str:
        if timestamp in self.d[key]:
            return self.d[key][timestamp]
        else:
            for ts in reversed(sorted(self.d[key])):
                if ts <= timestamp:
                    return self.d[key][ts]
        return ""


sol = TimeMap()

print(sol.set("foo", "bar", 1))  # None
print(sol.get("foo", 1))  # "bar"
print(sol.get("foo", 3))  # "bar"
print(sol.set("foo", "bar2", 4))  # None
print(sol.get("foo", 4))  # "bar2"
print(sol.get("foo", 5))  # "bar2"

# Using asserts for the official example
tm = TimeMap()
tm.set("foo", "bar", 1)
assert tm.get("foo", 1) == "bar"
assert tm.get("foo", 3) == "bar"
tm.set("foo", "bar2", 4)
assert tm.get("foo", 4) == "bar2"
assert tm.get("foo", 5) == "bar2"

# the leetcode case that failed: two values for one key, reads before,
# at, between and after their timestamps
tm = TimeMap()
tm.set("love", "high", 10)
tm.set("love", "low", 20)
assert tm.get("love", 5) == ""
assert tm.get("love", 10) == "high"
assert tm.get("love", 15) == "high"
assert tm.get("love", 20) == "low"
assert tm.get("love", 25) == "low"
