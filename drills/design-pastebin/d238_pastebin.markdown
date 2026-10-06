DRILL: Pastebin
TRAINS: design-pastebin

Design a paste service. A user enters a block of text and gets a randomly
generated link; a user enters a link and views the paste; a paste can
expire. Assume 10 million paste writes and 100 million paste reads per
month, text only, and 1.27 KB stored per paste. Write: (1) the writes per
second, the reads per second and the new content per month; (2) the path of
a create request, component by component, and where the text and where the
metadata are stored; (3) how the link is generated and why 7 characters are
enough for 3 years; (4) the path of a read; (5) how expired pastes are
deleted; (6) what serves the read load and what serves the write load once
the design is scaled.

REQUIRED: the three numbers, both request paths with the SQL table and the
object store, MD5 then Base 62 with 62^7, the expiry scan, the cache with
read replicas. Storing the paste text in the SQL row is the fail.

## Answer
