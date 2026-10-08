"""
URL: https://leetcode.com/problems/find-smallest-letter-greater-than-target/description/?envType=problem-list-v2&envId=vn57k9wr

744. Find Smallest Letter Greater Than Target

You are given an array of characters letters that is sorted in non-decreasing order, and a character target. There are at least two different characters in letters.

Return the smallest character in letters that is lexicographically greater than target. If such a character does not exist, return the first character in letters.

Example 1:

Input: letters = ["c","f","j"], target = "a"
Output: "c"
Explanation: The smallest character that is lexicographically greater than 'a' in letters is 'c'.

Example 2:

Input: letters = ["c","f","j"], target = "c"
Output: "f"
Explanation: The smallest character that is lexicographically greater than 'c' in letters is 'f'.

Example 3:

Input: letters = ["x","x","y","y"], target = "z"
Output: "x"
Explanation: There are no characters in letters that is lexicographically greater than 'z' so we return letters[0].

Constraints:

    2 <= letters.length <= 10^4
    letters[i] is a lowercase English letter.
    letters is sorted in non-decreasing order.
    letters contains at least two different characters.
    target is a lowercase English letter.

---

LEETCODE: Accepted (0 ms, 20.5 MB)
"""


# mu 0.7
# def nextGreatestLetter(letters: [str], target: str) -> str
#   for l in letters
#     if l > target
#       return l
#   return letters[0]

class Solution:
    def nextGreatestLetter(self, letters: list[str], target: str) -> str:
        for l in letters:
            if l > target:
                return l
        return letters[0]


sol = Solution()
print(sol.nextGreatestLetter(['c', 'f', 'j'], 'a'))
_l, _r = sol.nextGreatestLetter(['c', 'f', 'j'], 'a'), 'c'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['c', 'f', 'j'], 'c'), 'f'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['x', 'x', 'y', 'y'], 'z'), 'x'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'a', 'b', 'b'], 'a'), 'b'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b', 'c', 'd', 'e'], 'e'), 'a'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b', 'c', 'd', 'e'], 'd'), 'e'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b', 'c', 'd', 'e'], 'z'), 'a'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b', 'c', 'd', 'e'], 'a'), 'b'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'a', 'a', 'a', 'b'], 'a'), 'b'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['m', 'm', 'm', 'm', 'z'], 'm'), 'z'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], 'i'), 'j'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b'], 'b'), 'a'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b'], 'a'), 'b'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'b', 'c', 'd', 'e'], 'c'), 'd'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.nextGreatestLetter(['a', 'c', 'f', 'f', 'j'], 'f'), 'j'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
