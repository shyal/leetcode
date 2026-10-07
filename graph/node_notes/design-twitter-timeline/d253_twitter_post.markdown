REFERENCE: d253 Twitter Post
SOURCE: System Design Primer, "Design the Twitter timeline and search" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md

REQUIRED
- Post: Client to Web Server to Write API, which stores the tweet in the
  user's own timeline in a SQL database, then contacts the Fan Out Service.
- The Fan Out Service queries the User Graph Service for the user's followers,
  then stores the tweet in the home timeline of each follower in a Memory
  Cache: O(n), 1,000 followers is 1,000 inserts.
- It also stores the tweet in the Search Index Service, stores media in the
  Object Store, and sends notifications through the Notification Service,
  asynchronously over a Queue.
