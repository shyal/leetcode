DRILL: Query Cache Eviction
TRAINS: design-query-cache

Design a key-value cache that saves the results of the most recent search
queries of a search engine. Assume 10 million users, 10 billion queries per
month, 270 bytes per cached entry, and limited memory.

Name the eviction policy and the two data structures that implement it, with
what happens at each end of the list.

REQUIRED: LRU, the doubly-linked list with new entries at the head and
expiring entries at the tail, the hash table to the list nodes. Evicting by
insertion order is the fail.

## Answer
