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

# Dependencies

```
python3 -m venv .venv
. .venv/bin/activate

# for graphviz support in the termina (OSX instructions)
brew install aalib
brew install cmake pkg-config cairo pango gd librsvg expat gts

# Other requirements
pip3 install requirements.txt
```

# sitecustomize.py

I'm adding some pretty printing functionality, so if you want to use this repo as a template, then make sure you install sitecustomize.py where it should reside (`.venv/lib/pythonX.X/site-packages/sitecustomize.py`).

```python
import builtins
from typing import List, Optional
from rich import print as rich_print
from tabulate import tabulate

def _print(*args, **kwargs):
    is_table = all(type(x) is list for x in args[0])
    if is_table:
        kwargs['numalign'] = kwargs.get('numalign', 'center')
        kwargs['stralign'] = kwargs.get('stralign', 'center')
        kwargs['headers'] = kwargs.get('headers', [str(k) for k in range(len(args[0]))])
        kwargs['showindex'] = kwargs.get('showindex', range(len(args[0])))
        rich_print(tabulate(*args, **kwargs))
    else:
        rich_print(*args, **kwargs)

builtins.print = _print
builtins.List = List
builtins.Optional = Optional
builtins.print_table = _print
```
