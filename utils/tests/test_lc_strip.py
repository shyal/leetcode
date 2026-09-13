"""lc_submit --check over every filed solve: the code the stripper would
send, checked for names leetcode lacks. A shape the stripper has not met
(a helper class above Solution, a design class, a harness alias) shows up
here before it shows up as a NameError on leetcode. The list below is the
solves that genuinely cannot be sent: they call a harness drawing function
inside the class. A new entry is a stripper regression or a new such
solve; a stale one is a fix, and comes out."""

import glob
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIN = os.path.join(ROOT, "utils", "rs", "target", "release", "lc_submit")

DRAWING_INSIDE_THE_CLASS = {
    "p1046_Last_Stone_Weight_2025_10_13T07_44_22_668857_00_00Z.py": "draw_heap",
    "p143_Reorder_List_2025_10_09T09_54_24_913679_00_00Z.py": "draw_linked_list",
    "p1584_Min_Cost_to_Connect_All_Points_2025_11_09T09_20_08_818826_00_00Z.py": "draw_graphviz",
    "p210_Course_Schedule_II_2025_11_05T00_38_43_280026_00_00Z.py": "draw_graphviz",
    "p210_Course_Schedule_II_FAILED_2026_09_10T23_29_19_368769_00_00Z.py": "draw_ascii_graph",
    "p215_Kth_Largest_Element_in_an_Array_2025_10_01T21_36_57_881287.py": "draw_heap",
    "p215_Kth_Largest_Element_in_an_Array_2025_10_13T23_55_00_633244_00_00Z.py": "draw_heap",
    "p227_Basic_Calculator_II_FAILED_2026_08_18T23_51_13_723603_00_00Z.py": "draw_tree",
    "p310_Minimum_Height_Trees_2025_11_07T09_13_20_081069_00_00Z.py": "draw_graphviz",
    "p310_Minimum_Height_Trees_2025_11_09T08_25_21_052230_00_00Z.py": "draw_graphviz",
    "p310_Minimum_Height_Trees_2025_11_10T09_02_24_023743_00_00Z.py": "draw_graphviz",
    "p3607_Power_Grid_Maintenance_2025_11_06T02_23_35_167721_00_00Z.py": "draw_graphviz",
    "p701_Insert_into_a_Binary_Search_Tree_2025_10_09T23_56_02_925864_00_00Z.py": "draw_tree",
    "p743_Network_Delay_Time_2025_11_06T04_26_03_093729_00_00Z.py": "draw_graphviz",
    "p767_Reorganize_String_2025_10_14T02_37_54_600554_00_00Z.py": "draw_heap",
    "p802_Find_Eventual_Safe_States_2025_11_05T10_18_05_709286_00_00Z.py": "draw_graphviz",
    "p86_Partition_List_2025_10_09T20_38_35_470961_00_00Z.py": "draw_linked_list",
    "p947_Most_Stones_Removed_with_Same_Row_or_Column_2025_11_04T23_13_11_644520_00_00Z.py": "draw_graphviz",
    "p973_K_Closest_Points_to_Origin_2025_10_14T03_32_17_909605_00_00Z.py": "draw_heap",
}


def test_every_filed_solve_strips_to_what_leetcode_can_run():
    files = sorted(glob.glob(os.path.join(ROOT, "solved", "p*.py")))
    assert len(files) > 700
    p = subprocess.run(
        [BIN, "--check", *files], capture_output=True, text=True, cwd=ROOT
    )
    found = {}
    for line in p.stdout.splitlines():
        path, names = line.split(": ", 1)
        found[os.path.basename(path)] = names
    assert found == DRAWING_INSIDE_THE_CLASS
    assert p.returncode == 1
