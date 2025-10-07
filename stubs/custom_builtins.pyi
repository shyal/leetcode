"""Stub file for custom builtins additions."""

from typing import Any, Callable, Dict, Generic, Iterable, Iterator, List, Optional, Tuple, TypeVar, Union, overload

from collections import Counter as Counter, defaultdict as defaultdict

from functools import reduce as reduce

from itertools import accumulate as accumulate, chain as chain, combinations as combinations, groupby as groupby, pairwise as pairwise, permutations as permutations, product as product, takewhile as takewhile, zip_longest as zip_longest

from math import ceil as ceil, floor as floor, log10 as log10, log2 as log2, prod as prod

from operator import add as add, and_ as and_, or_ as or_, xor as xor

from heapq import heapify as heapify, heappop as heappop, heappush as heappush, nlargest as nlargest, nsmallest as nsmallest

from string import ascii_letters as ascii_letters, ascii_lowercase as ascii_lowercase, ascii_uppercase as ascii_uppercase

from re import match as match

from bisect import bisect_left as bisect_left, bisect_right as bisect_right

from rich import print as rich_print

from tabulate import tabulate

# Type aliases
Any = Any
Callable = Callable
Dict = Dict
Generic = Generic
Iterable = Iterable
Iterator = Iterator
List = List
Optional = Optional
Tuple = Tuple
TypeVar = TypeVar
Union = Union
overload = overload

# Class stubs
class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None) -> None: ...
    val: int
    left: Optional['TreeNode']
    right: Optional['TreeNode']

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None) -> None: ...
    val: int
    next: Optional['ListNode']

class Node:
    def __init__(self, val: Any, children: Dict[Any, 'Node'] = ...) -> None: ...
    val: Any
    children: Dict[Any, 'Node']

# dd is alias for defaultdict
dd = defaultdict

# String constants
ascii_letters: str
ascii_lowercase: str
ascii_uppercase: str

# Function stubs for shortcuts
def groupby(__iterable: Iterable[Any], __key: Optional[Callable[..., Any]] = None) -> Iterator[Tuple[Any, Iterator[Any]]]: ...

def combinations(__iterable: Iterable[Any], __r: int) -> Iterator[Tuple[Any, ...]]: ...

def log10(__x: float) -> float: ...

def log2(__x: float) -> float: ...

def floor(__x: float) -> int: ...

def ceil(__x: float) -> int: ...

def pairwise(__iterable: Iterable[Any]) -> Iterator[Tuple[Any, Any]]: ...

def zip_longest(*__iterables: Iterable[Any], fillvalue: Any = None) -> Iterator[Tuple[Any, ...]]: ...

def takewhile(__predicate: Callable[[Any], bool], __iterable: Iterable[Any]) -> Iterator[Any]: ...

def prod(__iterable: Iterable[int | float], *, start: int | float = 1) -> int | float: ...

def product(*__iterables: Iterable[Any], repeat: int = 1) -> Iterator[Tuple[Any, ...]]: ...

def enumr(__iterable: Iterable[Any], __start: int = 0) -> Iterator[Tuple[int, Any]]: ...

def accumulate(__iterable: Iterable[Any], __func: Optional[Callable[[Any, Any], Any]] = None, *, initial: Any = None) -> Iterator[Any]: ...

def bisect_left(__a: List[Any], __x: Any, __lo: int = 0, __hi: Optional[int] = None) -> int: ...

def bisect_right(__a: List[Any], __x: Any, __lo: int = 0, __hi: Optional[int] = None) -> int: ...

def chain(*__iterables: Iterable[Any]) -> Iterator[Any]: ...

def add(__a: Any, __b: Any) -> Any: ...

def xor(__a: Any, __b: Any) -> Any: ...

def heapify(__heap: List[Any]) -> None: ...

def heappop(__heap: List[Any]) -> Any: ...

def heappush(__heap: List[Any], __item: Any) -> None: ...

def nlargest(__n: int, __iterable: Iterable[Any], __key: Optional[Callable[[Any], Any]] = None) -> List[Any]: ...

def nsmallest(__n: int, __iterable: Iterable[Any], __key: Optional[Callable[[Any], Any]] = None) -> List[Any]: ...

def match(__pattern: str, __string: str, __flags: int = 0) -> Any: ...  # returns Match object or None

def permutations(__iterable: Iterable[Any], __r: Optional[int] = None) -> Iterator[Tuple[Any, ...]]: ...

def or_(__a: Any, __b: Any) -> Any: ...

def and_(__a: Any, __b: Any) -> Any: ...

# Pretty printing
def tabulate(tabular_data: Any, headers: Iterable[str] = ..., tablefmt: str = ..., **kwargs: Any) -> str: ...

def rich_print(*objects: Any, **kwargs: Any) -> None: ...

# Utils from tree_utils, bst_utils, linked_list_utils
def draw_tree(root: Optional[TreeNode]) -> None: ...

def draw_linked_list(head: Optional[ListNode]) -> None: ...

def draw_general_tree(root: Optional[Node]) -> None: ...

def build_tree(arr: List[Optional[int]]) -> Optional[TreeNode]: ...

def generate_and_print_random_bst(n: int, seed: Optional[int] = None, verbose: bool = True) -> Optional[TreeNode]: ...

def generate_full_binary_tree(height: int) -> Optional[TreeNode]: ...

def get_list_values(head: Optional[ListNode]) -> List[int]: ...

def print_linked_list(head: Optional[ListNode]) -> None: ...

def build_linked_list(vals: Iterable[int]) -> Optional[ListNode]: ...

def find_node(root: Optional[TreeNode], val: Any) -> Optional[TreeNode]: ...

def get_inorder(root: Optional[TreeNode]) -> List[int]: ...

def is_balanced(root: Optional[TreeNode]) -> bool: ...

def is_valid_bst(root: Optional[TreeNode]) -> bool: ...