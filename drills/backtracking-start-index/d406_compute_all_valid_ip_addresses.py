"""
EPI 6.9 Compute all valid IP addresses

Given a string s of digits, return every valid IP address that you can
make by putting three dots into s. A valid IP address is four parts
joined by '.', where each part is an integer from 0 to 255 with no
leading zero: "0" is a valid part, "00" and "01" are not. Return the
addresses in any order.

Example 1:

Input: s = "25511"
Output: ["2.5.5.11", "2.5.51.1", "2.55.1.1", "25.5.1.1"]

Example 2:

Input: s = "0100"
Output: ["0.1.0.0"]
Explanation: "01" and "00" have a leading zero, so the only split is
0, 1, 0, 0.

Example 3:

Input: s = "123"
Output: []
Explanation: three digits cannot make four parts.

Constraints:

    0 <= len(s) <= 1000
    s consists of digits only.

    REQUIRED: O(1) time for any len(s). NO regex, NO itertools.
"""


class Solution:
    def get_valid_ip_address(self, s: str) -> list[str]:
        pass


sol = Solution()

print(sol.get_valid_ip_address("25511"))  # ['2.5.5.11', '2.5.51.1', '2.55.1.1', '25.5.1.1']

# assert sorted(sol.get_valid_ip_address("25511")) == ["2.5.5.11", "2.5.51.1", "2.55.1.1", "25.5.1.1"]
# assert sol.get_valid_ip_address("0100") == ["0.1.0.0"]
# assert sol.get_valid_ip_address("123") == []
# assert sol.get_valid_ip_address("") == []
# assert sol.get_valid_ip_address("1234") == ["1.2.3.4"]
# assert sol.get_valid_ip_address("0000") == ["0.0.0.0"]
# assert sol.get_valid_ip_address("10000") == ["10.0.0.0"]
# assert sorted(sol.get_valid_ip_address("010010")) == ["0.10.0.10", "0.100.1.0"]
# assert sol.get_valid_ip_address("255255255255") == ["255.255.255.255"]
# assert sol.get_valid_ip_address("256256256256") == []
# assert sol.get_valid_ip_address("12345678901") == []
# assert sorted(sol.get_valid_ip_address("101023")) == ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"]
# assert sorted(sol.get_valid_ip_address("2552551113")) == ["255.25.51.113", "255.255.1.113", "255.255.11.13", "255.255.111.3"]
# assert sorted(sol.get_valid_ip_address("11111111111")) == ["11.111.111.111", "111.11.111.111", "111.111.11.111", "111.111.111.11"]
# assert len(sol.get_valid_ip_address("1921680")) == 11
# assert all(sol.get_valid_ip_address("1" * 1000) == [] for _ in range(1000))
