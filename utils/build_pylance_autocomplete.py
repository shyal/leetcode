import os
import re
from xai_sdk import Client
from xai_sdk.chat import system, user


def strip_triple_ticks(text: str) -> str:
    pattern = r"^```(?:\w+)?\n|```$"
    result = re.sub(pattern, "", text, flags=re.MULTILINE)
    return result.strip()


def grok(user_prompt):
    chat = client.chat.create(
        model="grok-4-0709",
        messages=[
            system(
                "You are a helpful assistant that generates Python stubs for LeetCode problems."
            ),
            user(user_prompt),
        ],
    )
    response = chat.sample()
    code = response.content
    return strip_triple_ticks(code)


api_key = os.getenv("GROK_API_KEY")
client = Client(api_key)

# Read the file contents
sitecustomize_content = open("utils/sitecustomize.py", "r").read()
types_content = open("utils/Types.py", "r").read()
tree_utils_content = open("utils/tree_utils.py", "r").read()
bst_utils_content = open("utils/bst_utils.py", "r").read()
linked_list_utils_content = open("utils/linked_list_utils.py", "r").read()

# Construct the prompt for Grok
user_prompt = f"""
Here is the content of utils/sitecustomize.py:
```python
{sitecustomize_content}
```

Here is the content of utils/Types.py:
```python
{types_content}
```

Here is the content of utils/tree_utils.py:
```python
{tree_utils_content}
```

Here is the content of utils/bst_utils.py:
```python
{bst_utils_content}
```

Here is the content of utils/linked_list_utils.py:
```python
{linked_list_utils_content}
```

Based on the sitecustomize.py, which adds various shortcuts, types, and utils to the builtins module, and using the actual definitions from the provided utils files, generate an updated version of stubs/custom_builtins.pyi.

The .pyi file should include:
- Necessary imports for typing and the custom modules.
- TypeVar definitions as needed.
- Type aliases for List, Optional, TreeNode, ListNode.
- Function stubs for all the shortcuts from itertools, math, collections, etc.
- Class stubs for Counter, defaultdict, etc.
- Function stubs for the pretty printing (tabulate, rich_print).
- Accurate function stubs for all utils from tree_utils, bst_utils, and linked_list_utils, based on their actual signatures in the provided code.

Do not include standard builtins definitions; only the custom additions.

Provide the complete content of the .pyi file, wrapped in ```python ... ``` for easy extraction.
"""

# Call Grok to get the updated custom_builtins.pyi
updated_custom_pyi = grok(user_prompt)

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
