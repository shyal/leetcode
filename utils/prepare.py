import subprocess
import os
import re
from xai_sdk import Client
from xai_sdk.chat import system, user


def run_git(cmd):
    """Run a git command and return its output."""
    try:
        return (
            subprocess.check_output(["git"] + cmd, stderr=subprocess.STDOUT)
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(cmd)}\nOutput: {e.output.decode()}")
        sys.exit(1)


api_key = os.getenv("GROK_API_KEY")
if not api_key:
    raise ValueError("GROK_API_KEY environment variable not set")

client = Client(api_key=api_key)

with open("today.txt") as f:
    content = f.read()
    today = content.split("URL: ")

problems = ["URL: " + ex.strip() for ex in today if ex.strip()]

for problem_text in problems:
    run_git(["checkout", "master"])
    lines = problem_text.splitlines()
    number = None
    problem_title = None
    for line in lines:
        match = re.match(r"(\d+)\. ", line.strip())
        if match:
            number = match.group(1)
            problem_title = line.strip()
            break
    if not number:
        print(f"Could not find exercise number in: {problem_text[:100]}...")
        continue

    # Prepare the prompt
    example_stub = '''
"""
URL: https://leetcode.com/problems/binary-tree-preorder-traversal/description/

144. Binary Tree Preorder Traversal

Given the root of a binary tree, return the preorder traversal of its nodes' values.


Example 1:

Input: root = [1,None,2,3]

Output: [1,2,3]

Explanation:

Example 2:

Input: root = [1,2,3,4,5,None,8,None,None,6,7,9]

Output: [1,2,4,5,6,7,3,8,9]

Explanation:

Example 3:

Input: root = []

Output: []

Example 4:

Input: root = [1]

Output: [1]


Constraints:

        The number of nodes in the tree is in the range [0, 100].
        -100 <= Node.val <= 100


Follow up: Recursive solution is trivial, could you do it iteratively?
"""


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        pass


sol = Solution()
tree = build_tree([1, None, 2, 3])
draw_tree(tree)
assert sol.preorderTraversal(tree) == [1, 2, 3]

sol = Solution()
tree = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
draw_tree(tree)
assert sol.preorderTraversal(tree) == [1, 2, 4, 5, 6, 7, 3, 8, 9]

sol = Solution()
tree = build_tree([])
draw_tree(tree)
assert sol.preorderTraversal(tree) == []

sol = Solution()
tree = build_tree([1])
draw_tree(tree)
assert sol.preorderTraversal(tree) == [1]
'''

    user_prompt = f"""Please generate a usable stub for the following LeetCode problem. The stub should include the problem description as a docstring, the Solution class with the method signature and pass, then instantiate sol = Solution(), and add assert statements for each example.

Here is an example of how the stub should look:

{example_stub}

Here is the `sitecustomize.py`. Use builtins when necessary.

{open('utils/sitecustomize.py').read()}

Now, for this problem:

{problem_text}

Output only the Python code for the stub, nothing else. Do not enclose your output in triple backticks (```). Indents are 4 spaces."""

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

    file_name = f"current.py"
    with open(file_name, "w") as f:
        f.write(code)

    print(f"Saved stub to {file_name}")

    run_git(["checkout", "-b", number])
    run_git(["add", "."])
    run_git(["commit", "-m", problem_title])
