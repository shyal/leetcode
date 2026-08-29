import os
import re
import subprocess as _subprocess


def strip_triple_ticks(text: str) -> str:
    pattern = r"^```(?:\w+)?\n|```$"
    result = re.sub(pattern, "", text, flags=re.MULTILINE)
    return result.strip()


def claude(user_prompt):
    result = _subprocess.run(
        ["claude", "-p", user_prompt, "--system-prompt",
         "You are a helpful assistant that generates Python stubs for LeetCode problems."],
        capture_output=True, text=True,
    )
    return strip_triple_ticks(result.stdout.strip())

# Read the file contents
sitecustomize_content = open("utils/harness/sitecustomize.py", "r").read()
types_content = open("utils/harness/Types.py", "r").read()
tree_utils_content = open("utils/harness/tree_utils.py", "r").read()
bst_utils_content = open("utils/harness/bst_utils.py", "r").read()
linked_list_utils_content = open("utils/harness/linked_list_utils.py", "r").read()

# Construct the prompt for Claude
user_prompt = f"""
Here is the content of utils/harness/sitecustomize.py:
```python
{sitecustomize_content}
```

Here is the content of utils/harness/Types.py:
```python
{types_content}
```

Here is the content of utils/harness/tree_utils.py:
```python
{tree_utils_content}
```

Here is the content of utils/harness/bst_utils.py:
```python
{bst_utils_content}
```

Here is the content of utils/harness/linked_list_utils.py:
```python
{linked_list_utils_content}
```

Based on the sitecustomize.py, which adds various shortcuts, types, and utils to the builtins module, and using the actual definitions from the provided utils files, generate an updated version of stubs/custom_builtins.pyi.

The .pyi file should include:
- Necessary imports for typing and the custom modules.
- TypeVar definitions as needed.
- Type aliases for Any, Dict, Generic, Iterable, Iterator, List, Optional, Tuple, TypeVar, Union, overload: you MUST use from typing import List as List etc. Import Callable as `from collections.abc import Callable as Callable` (never alias it as Collable).
- Function stubs for all the shortcuts from itertools, math, collections, etc.
- Class stubs for Counter, defaultdict, etc.
- Function stubs for the pretty printing (tabulate, rich_print).
- Accurate function stubs for all utils from tree_utils, bst_utils, and linked_list_utils, based on their actual signatures in the provided code.

Do not include standard builtins definitions; only the custom additions.

Provide the complete content of the .pyi file, wrapped in ```python ... ``` for easy extraction.
"""

# Call Claude to get the updated custom_builtins.pyi
updated_custom_pyi = claude(user_prompt)

# Save to stubs/custom_builtins.pyi
with open("stubs/custom_builtins.pyi", "w") as f:
    f.write(updated_custom_pyi)

# Read default_builtins.pyi
with open("stubs/default_builtins.pyi", "r") as f:
    default_pyi = f.read()

# Merge: default + custom
merged_content = (
    default_pyi
    + "\n\n# Custom additions for LeetCode utils and shortcuts\n"
    + updated_custom_pyi
)

# Save merged to stubs/builtins.pyi
with open("stubs/builtins.pyi", "w") as f:
    f.write(merged_content)

print("Successfully updated and merged stubs/builtins.pyi")
