"""
URL: https://leetcode.com/problems/determine-if-two-strings-are-close/description/?envType=problem-list-v2&envId=vn57k9wr

1657. Determine if Two Strings Are Close

Two strings are considered close if you can attain one from the other using the following operations:

1. Swap any two existing characters.
   For example, abcd e -> a e cd b

2. Transform every occurrence of one existing character into another existing character, and do the same with the other character.
   For example, aa c abb -> bb c baa (all a's turn into b's, and all b's turn into a's)

You can use the operations on either string as many times as necessary.

Given two strings, word1 and word2, return true if word1 and word2 are close, and false otherwise.

Example 1:

Input: word1 = "abc", word2 = "bca"
Output: true
Explanation: You can attain word2 from word1 in 2 operations.
Apply Operation 1: "a bc" -> "a cb"
Apply Operation 1: "a c b" -> "b c a"

Example 2:

Input: word1 = "a", word2 = "aa"
Output: false
Explanation: It is impossible to attain word2 from word1, or vice versa, in any number of operations.

Example 3:

Input: word1 = "cabbba", word2 = "abbccc"
Output: true
Explanation: You can attain word2 from word1 in 3 operations.
Apply Operation 1: "ca bbb a" -> "ca a bb b"
Apply Operation 2: "c aa bbb" -> "b aa ccc"
Apply Operation 2: "baa ccc" -> "abb ccc"

Constraints:

    1 <= word1.length, word2.length <= 10^5
    word1 and word2 contain only lowercase English letters.

---

Op 1 seems straight forward, swap any 2 characters

abcde -> aecdb
 ^  ^     ^  ^

Op 2 is more "interesting".

aacabb -> bbcbaa

In short: all as become bs, and all bs become as.

So that's for the transformations. So this is roughly the shape
of a BFS? Mutate word1 until it becomes word2. No need to return
a shortest path, just a bool if it can be achieved.

But... if order doesn't matter due to op 1, and counts are interchangeable
through op 2, then could this simply be a set comparison, and counts
comparison?

Let's try.

Yup that checks out.

Let's try on lc.

Nope. Failing case:

aaabbbbccddeeeeefffff
aaaaabbcccdddeeeeffff

Should be False, but is True. OH. Of course, the counts are actually bound to
character pairs.

{   'e': 5,
    'f': 5,
    'b': 4,
    'a': 3,
    'c': 2,
    'd': 2
}
{   'a': 5,
    'e': 4,
    'f': 4,
    'c': 3,
    'd': 3,
    'b': 2
}

So this becomes the new target. We need to swap counts until the dicts match.
Much simpler this way.

{
    'a': 3,
    'e': 5,
    'f': 5,
    'c': 2,
    'd': 2,
    'b': 4
}
{   'a': 5,
    'e': 4,
    'f': 4,
    'c': 3,
    'd': 3,
    'b': 2
}

So a single step would be swapping two values in a so the keys match the respective keys
in b, but we're not guaranteed that there's a match, since it may take multiple swaps.

But looking at the counts of counts, they seem to have the same shape.

Counter({2: 2, 3: 1, 4: 1, 5: 2})
Counter({2: 1, 3: 2, 4: 2, 5: 1})

2, 2, 1, 1

Passes on leetcode. So compare counters of counter values. Neat little trick + question.

"""


class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        a = Counter(word1)
        b = Counter(word2)
        return (
            len(word1) == len(word2)
            and set(a.keys()) == set(b.keys())
            and Counter(a.values()) == Counter(b.values())
        )


sol = Solution()

print(Solution().closeStrings("aaabbbccc", "cccbbbaaa"))

assert (
    sol.closeStrings("aaabbbbccddeeeeefffff", "aaaaabbcccdddeeeeffff") == False
)  # False
print(sol.closeStrings("abc", "bca"))  # True

assert sol.closeStrings("abc", "bca") == True
assert sol.closeStrings("a", "aa") == False
assert sol.closeStrings("cabbba", "abbccc") == True

assert Solution().closeStrings("", "") == True
assert Solution().closeStrings("a", "a") == True
assert Solution().closeStrings("a", "b") == False
assert Solution().closeStrings("aaabbbccc", "cccbbbaaa") == True
assert Solution().closeStrings("aaabbbccc", "aaabbbcccd") == False
assert Solution().closeStrings("abcabcabc", "cbacbacba") == True
assert Solution().closeStrings("zzzzzzzzzz", "zzzzzzzzzz") == True
assert Solution().closeStrings("aabbccddeeffgghhii", "hhggeeccbbddaaiif") == False
assert Solution().closeStrings("abc" * 33333 + "d", "abc" * 33333 + "e") == False
assert Solution().closeStrings("a" * 100000, "a" * 99999 + "b") == False
assert (
    Solution().closeStrings("a" * 50000 + "b" * 50000, "b" * 50000 + "a" * 50000)
    == True
)
assert Solution().closeStrings("abcde" * 20000, "edcba" * 20000) == True
