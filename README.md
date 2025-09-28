# Leetcode solutions

I've recently decided to track my leetcode progress using a git repo, as it seems this is a common approach with serious leetcoders.

Currently organizing solutions into:

```
leetcode_easy.py
leetcode_medium.py
leetcode_hard.py
```

`Easy`, `Medium` and `Hard` ratings are my own, not leetcode's.

The general format is:

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

# Dependencies

```
python3 -m venv .venv
. .venv/bin/activate
cp utils/sitecustomize.py .venv/lib/python3.10/site-packages/
pip3 install requirements.txt
```

# Running

```
PYTHONPATH=./utils:${PYTHONPATH} python3 utils/runner.py
```
