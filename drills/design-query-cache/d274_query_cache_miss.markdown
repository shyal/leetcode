DRILL: Query Cache Miss
TRAINS: design-query-cache

Design a key-value cache that saves the results of the most recent search
queries of a search engine. Assume 10 million users, 10 billion queries per
month, 270 bytes per cached entry, and limited memory.

Write the flow of a cache miss.

REQUIRED: the Reverse Index Service, the Document Service, the cache updated
with the entry at the front. Having the cache fetch the result itself is the
fail.

## Answer
