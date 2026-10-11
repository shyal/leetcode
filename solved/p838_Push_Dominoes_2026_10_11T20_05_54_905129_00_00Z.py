"""
URL: https://leetcode.com/problems/push-dominoes/description/?envType=problem-list-v2&envId=vn57k9wr

838. Push Dominoes

There are n dominoes in a line, and we place each domino vertically upright. In the beginning, we simultaneously push some of the dominoes either to the left or to the right.

After each second, each domino that is falling to the left pushes the adjacent domino on the left. Similarly, the dominoes falling to the right push their adjacent dominoes standing on the right.

When a vertical domino has dominoes falling on it from both sides, it stays still due to the balance of the forces.

For the purposes of this question, we will consider that a falling domino expends no additional force to a falling or already fallen domino.

You are given a string dominoes representing the initial state where:

- dominoes[i] = 'L', if the ith domino has been pushed to the left,
- dominoes[i] = 'R', if the ith domino has been pushed to the right, and
- dominoes[i] = '.', if the ith domino has not been pushed.

Return a string representing the final state.

Example 1:

Input: dominoes = "RR.L"
Output: "RR.L"
Explanation: The first domino expends no additional force on the second domino.

Example 2:

Input: dominoes = ".L.R...LR..L.."
Output: "LL.RR.LLRRLL.."

Constraints:

    n == dominoes.length
    1 <= n <= 10^5
    dominoes[i] is either 'L', 'R', or '.'.
---
Simulation, and it seems fairly simple on the outset:
Find the right most Rs followed by a ., and the Ls preceded by a .
For those R. propagage the R to the right with a temporary placeholder, e.g x
.L.R...LR..L.. becomes
.L.Rr..LRr.L.. same for .L
lL.Rr.lLRrlL.. then substitute
LL.RR.LLRRLL.. then do it again
LL.RRrLLRRLL.. 
LL.RRrLLRRLL.. this time around, the L has an r on its left, thus equilibrium, so substitues it to an x
LL.RRxLLRRLL.. the fallen count matches the x count, so we've reached a state of equilibrium
LL.RRxLLRRLL.. subsitute the xs back to . and we're done
LL.RRxLLRRLL.. 
LL.RR.LLRRLL.. (final)

This works fine, but TLE... great.

class Solution
  def pushDominoes(dominoes: str) -> str
    prev = dominoes
    while True
      dominoes = dominoes.replace('R.', 'Rr')
      dominoes = dominoes.replace('.L', 'lL')
      dominoes = dominoes.replace('rL', '.L')
      dominoes = dominoes.replace('r', 'R')
      dominoes = dominoes.replace('l', 'L')
      if dominoes == prev
        return dominoes
      prev = dominoes

unfinished solution. i give up.. and will stick with the TLE version for now.

class Solution
  def pushDominoes(dominoes: str) -> str
    dominoes = list(dominoes)
    n = len dominoes
    right_subs, left_subs = 0, 0
    print dominoes
    while True
      for ~i, v in dominoes
        if v == 'R' and i < n -1 and dominoes[i + 1] == '.'
          if i < n - 2 and dominoes[i + 2] == 'L'
            pass
          else
            dominoes[i+1] = 'R'
            right_subs += 1
      for ~i, v in dominoes
        if v == 'L' and i > 0 and dominoes[i - 1] == '.'
          if i > 1 and dominoes[i - 2] == 'R'
            pass
          else
            dominoes[i-1] = 'L'
            left_subs += 1
      print dominoes
      if left_subs + right_subs == 0
        return ''.join(dominoes)
      right_subs = 0
      left_subs = 0

LEETCODE: Time Limit Exceeded (44/45 cases)
"""


# mu 0.9
# class Solution
#   def pushDominoes(dominoes: str) -> str
#     prev = dominoes
#     while True
#       dominoes = dominoes.replace('R.', 'Rr')
#       dominoes = dominoes.replace('.L', 'lL')
#       dominoes = dominoes.replace('rL', '.L')
#       dominoes = dominoes.replace('r', 'R')
#       dominoes = dominoes.replace('l', 'L')
#       if dominoes == prev
#         return dominoes
#       prev = dominoes

class Solution:
    def pushDominoes(self, dominoes: str) -> str:
        prev = dominoes
        while True:
            dominoes = dominoes.replace('R.', 'Rr')
            dominoes = dominoes.replace('.L', 'lL')
            dominoes = dominoes.replace('rL', '.L')
            dominoes = dominoes.replace('r', 'R')
            dominoes = dominoes.replace('l', 'L')
            if dominoes == prev:
                return dominoes
            prev = dominoes


sol = Solution()
print(sol.pushDominoes('.....L'))
_l, _r = sol.pushDominoes('RR.L'), 'RR.L'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('.L.R...LR..L..'), 'LL.RR.LLRRLL..'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('L'), 'L'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('R'), 'R'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('.'), '.'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('...'), '...'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('R.L.R.L.R.L.'), 'R.L.R.L.R.L.'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.pushDominoes('...L...R...'), 'LLLL...RRRR'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
