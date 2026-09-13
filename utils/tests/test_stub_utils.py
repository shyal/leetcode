# The prepared stub builds a tree or linked list into a named variable, prints
# it (the harness draws it), then passes it. hoist_builders rewrites a
# generator's inline call into that shape; strip_solution must still find the
# first-example call after the rewrite.
from kg.stub_utils import hoist_builders, strip_solution

HEAD = '''"""URL: https://leetcode.com/problems/x/"""


class Solution:
    def mergeTrees(self, root1, root2):
        return root1

    def depth(self, root):
        return 1


sol = Solution()

'''


def test_hoists_into_parameter_names():
    code = HEAD + (
        "print(get_level_order(sol.mergeTrees(build_tree([1, 3]), build_tree([2]))))  # [3]\n"
        "assert sol.mergeTrees(build_tree([1]), build_tree([2]))\n"
    )
    out = hoist_builders(code)
    assert out == HEAD + (
        "root1 = build_tree([1, 3])\n"
        "print(root1)\n"
        "root2 = build_tree([2])\n"
        "print(root2)\n"
        "\n"
        "print(get_level_order(sol.mergeTrees(root1, root2)))  # [3]\n"
        "assert sol.mergeTrees(build_tree([1]), build_tree([2]))\n"
    )
    assert hoist_builders(out) == out


def test_default_name_and_existing_variable_gets_printed():
    code = HEAD + (
        "head = build_linked_list([1, 2])\n"
        "print(get_list_values(sol.other(head)))  # [1]\n"
    )
    assert hoist_builders(code) == HEAD + (
        "head = build_linked_list([1, 2])\n"
        "print(head)\n"
        "print(get_list_values(sol.other(head)))  # [1]\n"
    )
    code = HEAD + "print(sol.other(build_tree([1])))  # 1\n"
    assert hoist_builders(code) == HEAD + (
        "root = build_tree([1])\nprint(root)\n\nprint(sol.other(root))  # 1\n"
    )


def test_strip_keeps_hoisted_lines_live():
    code = hoist_builders(
        HEAD
        + "print(sol.depth(build_tree([1])))  # 1\nassert sol.depth(build_tree([1])) == 1\n"
    )
    stub = strip_solution(code)
    assert (
        "root = build_tree([1])\nprint(root)\n\nprint(sol.depth(root))  # 1\n" in stub
    )
    assert "# assert sol.depth(build_tree([1])) == 1" in stub
    assert "        pass\n" in stub
