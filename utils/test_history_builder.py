from rich import print
from history_builder import *


def test_all_files_present():
    solved = get_solved_problems()
    missing = []
    for (
        prob_num,
        prob_title,
        commit_date,
        solve_time,
        matching_file,
        file_content,
    ) in solved:
        if matching_file is None:
            print(prob_num, "missing files")
            assert False, "Missing files"

        parsed_content = parse_content(file_content)
        if "assert" in parsed_content[1]:
            print(parsed_content)
            assert False, f"Parsing issue in {matching_file}"
