"""
URL: https://leetcode.com/problems/longest-common-prefix-between-adjacent-strings-after-removals/description/?envType=problem-list-v2&envId=vn57k9wr

3598. Longest Common Prefix Between Adjacent Strings After Removals

You are given an array of strings words. For each index i in the range [0, words.length - 1], perform the following steps:

- Remove the element at index i from the words array.
- Compute the length of the longest common prefix among all adjacent pairs in the modified array.

Return an array answer, where answer[i] is the length of the longest common prefix between the adjacent pairs after removing the element at index i. If no adjacent pairs remain or if none share a common prefix, then answer[i] should be 0.

Example 1:

Input: words = ["jump","run","run","jump","run"]
Output: [3,0,0,3,3]

Explanation:
- Removing index 0:
  words becomes ["run", "run", "jump", "run"]
  Longest adjacent pair is ["run", "run"] having a common prefix "run" (length 3)
- Removing index 1:
  words becomes ["jump", "run", "jump", "run"]
  No adjacent pairs share a common prefix (length 0)
- Removing index 2:
  words becomes ["jump", "run", "jump", "run"]
  No adjacent pairs share a common prefix (length 0)
- Removing index 3:
  words becomes ["jump", "run", "run", "run"]
  Longest adjacent pair is ["run", "run"] having a common prefix "run" (length 3)
- Removing index 4:
  words becomes ["jump", "run", "run", "jump"]
  Longest adjacent pair is ["run", "run"] having a common prefix "run" (length 3)

Example 2:

Input: words = ["dog","racer","car"]
Output: [0,0,0]

Explanation:
- Removing any index results in an answer of 0.

Constraints:

    1 <= words.length <= 10^5
    1 <= words[i].length <= 10^4
    words[i] consists of lowercase English letters.
    The sum of words[i].length is smaller than or equal 10^5.
---
LEETCODE: Time Limit Exceeded (705/718 cases)
class Solution
  # brute force solution
  def longestCommonPrefix(words: [str]) -> [int]
    memo prefix_lenth(a, b)
      count = 0
      for ca, cb in zip(a, b)
        if ca == cb
          count += 1
        else
          break
      count    
    def longest_common_prefix(words, skip)
      arr = words[:skip] + words[skip + 1:]
      res = 0
      for a, b in zip(arr, arr[1:])
        res = max(res, prefix_lenth(a, b))
      res
    result = []
    for >i in words
      result.append(longest_common_prefix(words, i))
    result
"""


# mu 0.10
# class Solution
#   def longestCommonPrefix(words: [str]) -> [int]
#     memo prefix_lenth(a, b)
#       count = 0
#       for ca, cb in zip(a, b)
#         if ca == cb
#           count += 1
#         else
#           break
#       count
#
#     n = len(words)
#     prefix = table(n + 1)
#     for i in 2..n
#       prefix[i] = max(prefix[i - 1], prefix_lenth(words[i - 2], words[i - 1]))
#     suffix = table(n + 1)
#     for <i in words[:-1]
#       suffix[i] = max(suffix[i + 1], prefix_lenth(words[i], words[i + 1]))
#     result = []
#     for >i in words
#       bridge = 0 < i < n - 1 ? prefix_lenth(words[i - 1], words[i + 1]) : 0
#       result.append(max(prefix[i], suffix[i + 1], bridge))
#     result

import sys
import threading


sys.setrecursionlimit(1 << 20)


def cache(fn):
    """Memoise fn on its arguments. Pure Python, so a deep memo recursion
    is not cut short by the C recursion limit of Python 3.12 and 3.13."""
    memo = {}

    def cached(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items()))) if kwargs else args
        if key not in memo:
            memo[key] = fn(*args, **kwargs)
        return memo[key]

    cached.__name__, cached.__doc__, cached.__wrapped__ = fn.__name__, fn.__doc__, fn
    return cached


def deep(fn):
    """Run fn on a thread with a 256 MB stack, so deep memo recursion fits."""
    out, err = [], []

    def target():
        try:
            out.append(fn())
        except BaseException as e:
            err.append(e)

    threading.stack_size(1 << 28)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if err:
        raise err[0]
    return out[0]


def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


class Solution:
    def longestCommonPrefix(self, words: list[str]) -> list[int]:
        def run():
            @cache
            def prefix_lenth(a, b):
                count = 0
                for ca, cb in zip(a, b):
                    if ca == cb:
                        count += 1
                    else:
                        break
                return count
            n = len(words)
            prefix = table(n + 1)
            for i in range(2, n + 1):
                prefix[i] = max(prefix[i - 1], prefix_lenth(words[i - 2], words[i - 1]))
            suffix = table(n + 1)
            for i in range(len(words[:-1]) - 1, -1, -1):
                suffix[i] = max(suffix[i + 1], prefix_lenth(words[i], words[i + 1]))
            result = []
            for i in range(len(words)):
                bridge = prefix_lenth(words[i - 1], words[i + 1]) if 0 < i < n - 1 else 0
                result.append(max(prefix[i], suffix[i + 1], bridge))
            return result
        return deep(run)


sol = Solution()
print(sol.longestCommonPrefix(['jump', 'run', 'run', 'jump', 'run']))


# FAILED: walked away after 30m 48s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
