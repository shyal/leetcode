DRILL: Pastebin Scaled
TRAINS: design-pastebin

Design a paste service. A user enters a block of text and gets a randomly
generated link; a user enters a link and views the paste; a paste can expire.
Assume 10 million paste writes and 100 million paste reads per month, text
only, and 1.27 KB stored per paste.

Say what serves the read load and what serves the write load once the design
is scaled.

REQUIRED: the cache, the read replicas, one master-slave for the writes.
Sharding the writes at 4 per second is the fail.

## Answer
