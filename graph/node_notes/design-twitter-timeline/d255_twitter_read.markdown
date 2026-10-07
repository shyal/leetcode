REFERENCE: d255 Twitter Read
SOURCE: System Design Primer, "Design the Twitter timeline and search" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md

REQUIRED
- Read: Client to Web Server to Read API to the Timeline Service, which gets
  the timeline of tweet ids and user ids from the Memory Cache in O(1), then
  multigets the Tweet Info Service and the User Info Service, O(n).

ALSO TRUE
- Search: Search API to the Search Service, which tokenizes the query and
  scatter gathers a Search Cluster such as Lucene, then merges, ranks and
  sorts.
