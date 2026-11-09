"""
EPI 15.2 Compute all mnemonics for a phone number

Given a string phone_number of digits, return every string that spells
it on a phone keypad, in any order. Each digit becomes one character of
its key:

    0: 0      1: 1      2: ABC    3: DEF    4: GHI
    5: JKL    6: MNO    7: PQRS   8: TUV    9: WXYZ

Example 1:

Input: phone_number = "23"
Output: ["AD", "AE", "AF", "BD", "BE", "BF", "CD", "CE", "CF"]

Example 2:

Input: phone_number = "207"
Output: ["A0P", "A0Q", "A0R", "A0S", "B0P", "B0Q", "B0R", "B0S", "C0P",
         "C0Q", "C0R", "C0S"]
Explanation: the key of 0 holds only "0".

Example 3:

Input: phone_number = "1"
Output: ["1"]

Constraints:

    1 <= len(phone_number) <= 8
    phone_number holds only the characters '0' to '9'.

    REQUIRED: O(len(phone_number) * 4^len(phone_number)) time. NO
    itertools.product.
"""


class Solution:
    def phone_mnemonic(self, phone_number: str) -> list[str]:
        pass


sol = Solution()

print(sol.phone_mnemonic("23"))  # ['AD', 'AE', 'AF', 'BD', 'BE', 'BF', 'CD', 'CE', 'CF']

# assert sorted(sol.phone_mnemonic("23")) == ["AD", "AE", "AF", "BD", "BE", "BF", "CD", "CE", "CF"]
# assert sorted(sol.phone_mnemonic("207")) == ["A0P", "A0Q", "A0R", "A0S", "B0P", "B0Q", "B0R", "B0S", "C0P", "C0Q", "C0R", "C0S"]
# assert sol.phone_mnemonic("1") == ["1"]
# assert sol.phone_mnemonic("0") == ["0"]
# assert sol.phone_mnemonic("10") == ["10"]
# assert sorted(sol.phone_mnemonic("2")) == ["A", "B", "C"]
# assert sorted(sol.phone_mnemonic("7")) == ["P", "Q", "R", "S"]
# assert sorted(sol.phone_mnemonic("9")) == ["W", "X", "Y", "Z"]
# assert sorted(sol.phone_mnemonic("19")) == ["1W", "1X", "1Y", "1Z"]
# assert sorted(sol.phone_mnemonic("88")) == ["TT", "TU", "TV", "UT", "UU", "UV", "VT", "VU", "VV"]
# words = sol.phone_mnemonic("2276696")
# assert len(words) == 3888 and len(set(words)) == 3888
# assert "ACRONYM" in words
# words = sol.phone_mnemonic("77779999")
# assert len(words) == 65536 and len(set(words)) == 65536
# assert "PQRSWXYZ" in words and "SSSSZZZZ" in words
# assert all(len(w) == 8 for w in words)
# words = sol.phone_mnemonic("01010101")
# assert words == ["01010101"]
