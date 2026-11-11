# URL: https://leetcode.com/problems/satisfiability-of-equality-equations/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 990. Satisfiability of Equality Equations
#
# You are given an array of strings equations that represent relationships between variables where each string equations[i] is of length 4 and takes one of two different forms: "xi==yi" or "xi!=yi". Here, xi and yi are lowercase letters (not necessarily different) that represent one-letter variable names.
#
# Return true if it is possible to assign integers to variable names so as to satisfy all the given equations, or false otherwise.
#
# Example 1:
#
# Input: equations = ["a==b","b!=a"]
# Output: false
# Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
# There is no way to assign the variables to satisfy both equations.
#
# Example 2:
#
# Input: equations = ["b==a","a==b"]
# Output: true
# Explanation: We could assign a = 1 and b = 1 to satisfy both equations.
#
# Constraints:
#
#     1 <= equations.length <= 500
#     equations[i].length == 4
#     equations[i][0] is a lowercase letter.
#     equations[i][1] is either '=' or '!'.
#     equations[i][2] is '='.
#     equations[i][3] is a lowercase letter.
#
# ---
# learning

# mu 0.17

class Solution
  def equationsPossible(equations: [str]) -> bool
    parent = {}
    def find(x)
      if parent.setdefault(x, x) == x
        return x
      parent[x] = find(parent[x])
      parent[x]
    for e in equations
      if e[1] == '='
        parent[find(e[0])] = find(e[-1])
    for e in equations
      if e[1] == '!' and find(e[0]) == find(e[-1])
        return false
    true

    


sol = Solution()

print(sol.equationsPossible(['a==b', 'b!=a']))  # False

assert sol.equationsPossible(['a==b', 'b!=a']) == false
assert sol.equationsPossible(['b==a', 'a==b']) == true

assert sol.equationsPossible(['a==a']) == true
assert sol.equationsPossible(['a!=a']) == false
assert sol.equationsPossible(['a==b', 'b==c', 'c==a', 'a!=c']) == false
assert sol.equationsPossible(['a==b', 'b!=c', 'c==a']) == false
assert sol.equationsPossible(['a==b'] * 500) == true
assert sol.equationsPossible(['a!=b'] * 500) == true
assert sol.equationsPossible(['a==b', 'b==c', 'c!=a']) == false
assert sol.equationsPossible(['a==b', 'b==c', 'c==d', 'd!=a']) == false
assert sol.equationsPossible(['a==b', 'b!=c', 'c==d', 'd!=a']) == true
assert sol.equationsPossible(['a==b', 'b==c', 'c==d', 'd==e', 'e==f', 'f==g', 'g==h', 'h==i', 'i==j', 'j==k', 'k==l', 'l==m', 'm==n', 'n==o', 'o==p', 'p==q', 'q==r', 'r==s', 's==t', 't==u', 'u==v', 'v==w', 'w==x', 'x==y', 'y==z', 'a!=z']) == false
assert sol.equationsPossible(['a==b', 'b!=c', 'c==d', 'd!=e', 'e==f', 'f!=g', 'g==h', 'h!=i', 'i==j', 'j!=k', 'k==l', 'l!=m', 'm==n', 'n!=o', 'o==p', 'p!=q', 'q==r', 'r!=s', 's==t', 't!=u', 'u==v', 'v!=w', 'w==x', 'x!=y', 'y==z']) == true
assert sol.equationsPossible(['a==a', 'b==b', 'c==c', 'd==d', 'e==e', 'f==f', 'g==g', 'h==h', 'i==i', 'j==j', 'k==k', 'l==l', 'm==m', 'n==n', 'o==o', 'p==p', 'q==q', 'r==r', 's==s', 't==t', 'u==u', 'v==v', 'w==w', 'x==x', 'y==y', 'z==z']) == true
