DRILL: Query Cache
TRAINS: design-query-cache

Design a key-value cache that saves the results of the most recent search
queries of a search engine. Assume 10 million users, 10 billion queries per
month, 270 bytes per cached entry, and limited memory. Write: (1) the
requests per second and the cache data per month if every query were unique
and stored; (2) the eviction policy and the two data structures that
implement it, with what happens at each end; (3) the flow of a hit and the
flow of a miss; (4) three events after which a cached entry should be
updated, and the simplest way to handle them; (5) the three ways to store
the cache on many machines, the trade of each, and the one to choose.

REQUIRED: two numbers, LRU with the doubly-linked list and the hash table,
both flows, three events with the TTL, three layouts with the sharded one
chosen. Evicting by insertion order is the fail.

## Answer
