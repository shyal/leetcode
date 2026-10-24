Design a paste service. A user enters a block of text and gets a randomly
generated link; a user enters a link and views the paste; a paste can expire.
Assume 10 million paste writes and 100 million paste reads per month, text
only, and 1.27 KB stored per paste.

Say how the link is generated and why 7 characters are enough for 3 years.

REQUIRED: MD5 then Base 62, the first 7 characters, 62^7 against the links of
3 years. Base 64, whose + and / need escaping in a url, is the fail.

## Answer
