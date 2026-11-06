"""
Given a string ip, return True when ip is an IPv4 address in dotted
form, otherwise False. The form is four parts separated by three '.'
characters. Each part is a run of one or more decimal digits with a
value from 0 to 255, and has no leading zero unless the part is "0".

Example 1:

Input: ip = "192.168.0.01"
Output: False
Explanation: "01" has a leading zero.

Example 2:

Input: ip = "255.255.255.255"
Output: True

Example 3:

Input: ip = "1.2.3.0x1"
Output: False
Explanation: "0x1" holds characters that are not decimal digits.

Constraints:

    0 <= len(ip) <= 100
    ip consists of printable ASCII characters.

    REQUIRED: O(len(ip)) time. NO regular expressions, NO ipaddress or
    socket module.
"""


class Solution:
    def validateIP(self, ip: str) -> bool:
        pass


sol = Solution()

print(sol.validateIP("192.168.0.01"))  # False

# assert sol.validateIP("192.168.0.01") is False
# assert sol.validateIP("255.255.255.255") is True
# assert sol.validateIP("1.2.3.0x1") is False
# assert sol.validateIP("192.168.0.1") is True
# assert sol.validateIP("0.0.0.0") is True
# assert sol.validateIP("123.24.59.99") is True
# assert sol.validateIP("192.168.123.456") is False
# assert sol.validateIP("1.2.3.4.5") is False
# assert sol.validateIP("1..23.4") is False
# assert sol.validateIP("123.256.34.56") is False
# assert sol.validateIP(".254.255.0") is False
# assert sol.validateIP("") is False
# assert sol.validateIP("1.2.3") is False
# assert sol.validateIP("1.2.3.4.") is False
# assert sol.validateIP(" 1.2.3.4") is False
# assert sol.validateIP("1.2.3.4 ") is False
# assert sol.validateIP("1.2.3.-4") is False
# assert sol.validateIP("1.2.3.+4") is False
# assert sol.validateIP("256.0.0.0") is False
# assert sol.validateIP("1.2.3.00") is False
# assert sol.validateIP("01.2.3.4") is False
# assert sol.validateIP("1.2.3.4a") is False
# assert sol.validateIP("1,2,3,4") is False
# assert sol.validateIP("1.2.3.0001") is False
# assert sol.validateIP("100.200.250.255") is True
