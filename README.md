# Leetcode solutions

I've recently decided to track my leetcode progress using a git repo, as it seems this is a common approach with serious leetcoders.

For now, all solutions are in `leetcode.py`, the general format is:

```
"""
[exercise link]
[exercise description]
"""
[imports]

class Solution():
    def ...():
        ...

sol = Solution()
sol....()

assert sol....() == [test case]
```

This approach is straight forward, and means i can easily review past solutions when scrolling. When i get stuck on a problem i check it into a branch.

I'm considering move the tests into a separate file, but have to weigh the pros and cons of that carefully.
