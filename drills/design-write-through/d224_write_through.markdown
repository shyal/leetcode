DRILL: Write Through
TRAINS: design-write-through

Write the three steps of a write under write-through. Say which component
the application treats as its main data store and which component writes to
the database. State what it does to write latency, to later reads, and to
staleness. Give two disadvantages.

REQUIRED: three steps with the synchronous write, the cache as the store the
application uses, slow writes with fresh fast reads, two disadvantages.
Making the database write asynchronous is the fail: that is write-behind.

## Answer
