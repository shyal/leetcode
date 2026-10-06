REFERENCE: d239 Twitter Timeline
SOURCE: System Design Primer, "Design the Twitter timeline and search" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md

REQUIRED
- 6,000 tweets per second, 60,000 tweets delivered on fanout per second,
  100,000 read requests per second, 4,000 search requests per second.
- Post: Client to Web Server to Write API, which stores the tweet in the
  user's own timeline in a SQL database, then contacts the Fan Out Service.
- The Fan Out Service queries the User Graph Service for the user's
  followers, then stores the tweet in the home timeline of each follower in
  a Memory Cache: O(n), 1,000 followers is 1,000 inserts.
- It also stores the tweet in the Search Index Service, stores media in the
  Object Store, and sends notifications through the Notification Service,
  asynchronously over a Queue.
- Home timelines live in a Memory Cache, a Redis list, because 60,000 fanout
  writes per second would overload a relational database; the store must
  have fast writes.
- Read: Client to Web Server to Read API to the Timeline Service, which gets
  the timeline of tweet ids and user ids from the Memory Cache in O(1), then
  multigets the Tweet Info Service and the User Info Service, O(n).
- Bottleneck: the Fan Out Service. A user with millions of followers takes
  minutes to fan out, which can race with replies; re-order the tweets at
  serve time.
- Or do not fan out the tweets of highly-followed users: search for their
  tweets, merge the results with the home timeline, and re-order at serve
  time.
- Two memory bounds out of: keep only several hundred tweets per home
  timeline in the cache; keep only active users' home timelines and rebuild
  the others from the SQL Database; store only a month of tweets in the
  Tweet Info Service; store only active users in the User Info Service.

ALSO TRUE
- 150 TB of new tweet content per month at about 10 KB per tweet with media.
- Search: Search API to the Search Service, which tokenizes the query and
  scatter gathers a Search Cluster such as Lucene, then merges, ranks and
  sorts.
- The user's own timeline is read from the SQL Database.
