from rich import print
from history.history_builder import *


def test_all_files_present():
    solved = get_solved_problems()
    missing = []
    seen = set([])
    for p in solved:
        if p.file is None:
            print(p.num, "missing files")
            assert False, "Missing files"

        if p.file in seen:
            print(p.num, p.file, "is not unique")
            # assert False, "Not unique"

        seen.add(p.file)

        parsed_content = parse_content(p.content)
        # test code leaking into the solution body shows up as top-level asserts;
        # asserts inside methods are legit (e.g. cross-checking two variants)
        if any(isinstance(node, ast.Assert) for node in ast.parse(parsed_content[1]).body):
            print(parsed_content)
            assert False, f"Parsing issue in {p.file}"


if __name__ == "__main__":
    test_all_files_present()
