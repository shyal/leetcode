# parse.py

import re


def extract_sections(lines):
    sections = []
    preamble = []
    i = 0
    first_section_start = None
    while i < len(lines):
        line = lines[i].strip()
        if line == '"""' or line.startswith('"""'):
            if first_section_start is None:
                first_section_start = i
                preamble = lines[:i]
            # start of docstring
            section_start = i
            doc_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('"""'):
                doc_lines.append(lines[i])
                i += 1
            i += 1  # skip the closing """
            # now find class Solution
            while i < len(lines) and not lines[i].strip().startswith("class Solution"):
                i += 1
            if i >= len(lines):
                break
            # now at class Solution, continue to collect until next """ or end
            j = i
            while j < len(lines):
                if lines[j].strip() == '"""' or lines[j].strip().startswith('"""'):
                    break
                j += 1
            section_end = j
            section_lines = lines[section_start:section_end]
            # extract number
            number = None
            title = None
            for dline in doc_lines:
                dline = dline.strip()
                if dline:
                    match = re.match(r"(\d+)\.\s*(.+)", dline)
                    if match:
                        number = int(match.group(1))
                        title = dline
                        break
            if number is None:
                # check for url then next line
                for k in range(len(doc_lines)):
                    if doc_lines[k].strip().startswith("https://"):
                        if k + 1 < len(doc_lines):
                            next_line = doc_lines[k + 1].strip()
                            match = re.match(r"(\d+)\.\s*(.+)", next_line)
                            if match:
                                number = int(match.group(1))
                                title = next_line
                                break
            if number is not None:
                sections.append((number, section_lines))
            i = section_end
        else:
            i += 1
    return preamble, sections


if __name__ == "__main__":
    with open("leetcode.py", "r") as f:
        lines = f.readlines()

    preamble, sections = extract_sections(lines)

    # sort sections by number
    sections.sort(key=lambda x: x[0])

    # flatten sorted section lines
    sorted_section_lines = []
    for _, sec in sections:
        sorted_section_lines.extend(sec)

    # write back to file
    with open("leetcode.py", "w") as f:
        f.writelines(preamble + sorted_section_lines)
