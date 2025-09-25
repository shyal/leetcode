from typing import Callable, Iterable, Any, TypeVar

from PrettyPrint.PrintTree.HorizontalTree import (
    join_vertically,
    add_parent as add_parent_left,
)
from PrettyPrint.PrintTree.VerticalTree import (
    join_horizontally,
    add_parent as add_parent_top,
)
from PrettyPrint.Utils.NodeFormatter import NodeFormatter
from PrettyPrint.Utils.Orientation import Orientation
from PrettyPrint.Utils.StyleAwareUtils import trim_text

T = TypeVar("T")

# ANSI escape codes for connector foreground colors
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


class TreeFormatter:
    def __init__(
        self,
        get_children: Callable[[T], Iterable[T]],
        get_val: Callable[[T], Any],
        get_label: Callable[[T], Any],
        label_color: str,
        show_newline_literal: bool,
        newline_literal: str,
        trim: int,
        trim_symbol: str,
        start_message: Callable[[T], str],
        color: str,
        border: bool,
        max_depth: int,
        orientation: bool,
    ):
        self.get_children = get_children
        self.get_node_val = get_val
        self.get_label = get_label
        self.label_color = label_color
        self.trim = trim
        self.trim_symbol = trim_symbol
        self.show_newline = show_newline_literal
        self.newline_literal = newline_literal
        self.start_message = start_message
        self.color = color
        self.border = border
        self.max_depth = max_depth
        self.orientation = orientation

    def format(self, node: T) -> str:
        if self.orientation == Orientation.Vertical:
            res = self.tree_vertical_join(node)
        else:
            res = self.tree_horizontal_join(node)
        res = res.to_str().rstrip()
        if self.start_message:
            return f"{ self.start_message(node) }\n{ res }"
        return res

    def tree_vertical_join(
        self, tree_node: T, depth: int = 0, is_left: bool | None = None
    ) -> NodeFormatter:
        """
        tree_node: actual user tree node (T)
        returns: NodeFormatter for the subtree rooted at tree_node
        is_left: whether tree_node itself is a left child of its parent (used to color the connector to its parent)
        """
        label = self.get_label(tree_node) if self.get_label else None

        # Get raw children as provided by get_children (may omit None)
        children_raw = list(self.get_children(tree_node))

        # Create NodeFormatter for current node (styles/colors/trim etc.)
        node = self.add_styles(tree_node)

        if children_raw and (self.max_depth == -1 or depth < self.max_depth):
            # Build formatted children and remember whether each child is left/right
            children_with_flags = []
            for i, child in enumerate(children_raw):
                # Determine is_left flag correctly for binary trees:
                # - If two children are present, index 0 is left, index 1 is right.
                # - If only one child is present, try to inspect tree_node.left/right attributes.
                if len(children_raw) == 2:
                    child_is_left = i == 0
                elif len(children_raw) == 1:
                    left_attr = getattr(tree_node, "left", object())
                    right_attr = getattr(tree_node, "right", object())
                    if child is left_attr:
                        child_is_left = True
                    elif child is right_attr:
                        child_is_left = False
                    else:
                        # Fallback (best-effort): treat single child as left if we can't detect
                        child_is_left = i == 0
                else:
                    # No children (shouldn't reach here because children_raw is truthy)
                    child_is_left = None

                child_fmt = self.tree_vertical_join(
                    child, depth + 1, is_left=child_is_left
                )
                children_with_flags.append((child_fmt, child_is_left))

            if len(children_with_flags) == 1:
                # Single-child case: insert a colored '|' connector above the child
                child_node_fmt, child_is_left = children_with_flags[0]
                if child_is_left is True:
                    edge_str = f"{RED}/{RESET}"
                elif child_is_left is False:
                    edge_str = f"{BLUE}\\{RESET}"
                else:
                    edge_str = "|"
                child_node_fmt.lines.insert(
                    0, " " * child_node_fmt.get_middle_width() + edge_str
                )
                children_node = child_node_fmt
            else:
                # Two children: join them horizontally (we rely on join_horizontally for placement)
                children_node = join_horizontally(
                    [fmt for fmt, _ in children_with_flags]
                )

            node = add_parent_top(node, children_node)

        node = self.add_label(label, node, add_parent_top, "|")
        return node

    def tree_horizontal_join(
        self, tree_node: T, depth: int = 0, is_left: bool | None = None
    ) -> NodeFormatter:
        """
        Horizontal join variant (similar logic to vertical).
        """
        label = self.get_label(tree_node) if self.get_label else None
        children_raw = list(self.get_children(tree_node))
        node = self.add_styles(tree_node)
        node_padding = " " * node.width
        node.lines = node.lines + [node_padding]
        node.height += 1

        if children_raw and (self.max_depth == -1 or depth < self.max_depth):
            children_with_flags = []
            for i, child in enumerate(children_raw):
                if len(children_raw) == 2:
                    child_is_left = i == 0
                elif len(children_raw) == 1:
                    left_attr = getattr(tree_node, "left", object())
                    right_attr = getattr(tree_node, "right", object())
                    if child is left_attr:
                        child_is_left = True
                    elif child is right_attr:
                        child_is_left = False
                    else:
                        child_is_left = i == 0
                else:
                    child_is_left = None

                child_fmt = self.tree_horizontal_join(
                    child, depth + 1, is_left=child_is_left
                )
                children_with_flags.append((child_fmt, child_is_left))

            if len(children_with_flags) == 1:
                children_node, child_is_left = children_with_flags[0]
                middle = children_node.get_middle_height()
                new_lines = []
                for r_idx, line in enumerate(children_node.lines):
                    if r_idx == middle:
                        if child_is_left is True:
                            edge_str = f"{RED}─{RESET}"
                        elif child_is_left is False:
                            edge_str = f"{BLUE}─{RESET}"
                        else:
                            edge_str = "─"
                        new_lines.append(edge_str + line)
                    else:
                        new_lines.append(" " + line)
                children_node.lines = new_lines
            else:
                children_node = join_vertically([fmt for fmt, _ in children_with_flags])

            node = add_parent_left(node, children_node)

        node = self.add_label(label, node, add_parent_left, "─")
        return node

    def add_label(
        self,
        label: Any,
        node: NodeFormatter,
        parent_adder: Callable[[NodeFormatter, NodeFormatter], NodeFormatter],
        seperator: str,
    ) -> NodeFormatter:
        if label:
            label = NodeFormatter.from_string(str(label))
            if self.label_color:
                label.color_bg(self.label_color, True)
            node = parent_adder(NodeFormatter.from_string(seperator), node)
            node = parent_adder(label, node)
        return node

    def add_styles(self, tree_node: T) -> NodeFormatter:
        """
        Build and return a NodeFormatter for the given tree node (apply trim, newline literal, background color, border).
        """
        contents = str(self.get_node_val(tree_node))
        if self.show_newline:
            contents = contents.replace("\n", self.newline_literal)
        if self.trim != -1:
            contents = trim_text(contents, self.trim, self.trim_symbol)
        node = NodeFormatter.from_string(contents)
        if self.border:
            node.add_border()
        if self.color:
            node.color_bg(self.color, add_space=not self.border)
        return node
