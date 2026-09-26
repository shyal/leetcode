import pytest
from tree_utils import generate_random_tree, get_level_order


def count(root):
    return 0 if root is None else 1 + count(root.left) + count(root.right)


def height(root):
    return -1 if root is None else 1 + max(height(root.left), height(root.right))


def inorder(root):
    return [] if root is None else inorder(root.left) + [root.val] + inorder(root.right)


def test_size_and_values():
    root = generate_random_tree(10, seed=1)
    assert count(root) == 10
    assert sorted(v for v in get_level_order(root) if v is not None) == list(
        range(1, 11)
    )
    assert generate_random_tree(0) is None


def test_seed_fixes_the_tree():
    a = get_level_order(generate_random_tree(15, seed=7, sparsity=0.5))
    b = get_level_order(generate_random_tree(15, seed=7, sparsity=0.5))
    assert a == b


def test_sparsity_extremes():
    assert height(generate_random_tree(15, seed=3, sparsity=0.0)) == 3
    assert height(generate_random_tree(15, seed=3, sparsity=1.0)) == 14


def test_skew():
    chain = generate_random_tree(6, seed=3, sparsity=1.0, skew=-1.0)
    node, n = chain, 0
    while node:
        assert node.right is None
        node, n = node.left, n + 1
    assert n == 6
    chain = generate_random_tree(6, seed=3, sparsity=1.0, skew=1.0)
    assert chain is not None and chain.right is not None
    assert chain.left is None and chain.right.left is None


def test_bst_and_given_values():
    root = generate_random_tree(20, seed=5, sparsity=0.4, bst=True)
    assert inorder(root) == list(range(1, 21))
    root = generate_random_tree(3, seed=5, values=[9, 4, 7])
    assert get_level_order(root) == [9, 4, 7]
    with pytest.raises(ValueError):
        generate_random_tree(3, values=[1])


def test_node_parent_links_into_children():
    from Types import Node

    root = Node("main")
    a = Node({"fid": 0}, parent=root)
    b = Node({"fid": 1}, parent=a)
    assert root.children == {0: a}
    assert a.children == {0: b}
    assert b.children == {}


def test_general_tree_nested_form_round_trips():
    from tree_utils import build_general_tree, get_general_tree

    nested = [
        {},
        [[{"id": 0, "dur": 7}, [[{"id": 1, "dur": 4}, []]]], [{"id": 2, "dur": 1}, []]],
    ]
    root = build_general_tree(nested)
    assert root.children[0].children[0].val == {"id": 1, "dur": 4}
    assert get_general_tree(root) == nested
    assert get_general_tree(None) is None
