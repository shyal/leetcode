Design the Twitter timeline. A user posts a tweet; a user views the home
timeline, the tweets of the people they follow; a user views their own
timeline; a user searches keywords. Assume 100 million active users, 500
million tweets per day, an average fanout of 10 deliveries per tweet, 250
billion read requests and 10 billion searches per month.

Write the path of posting a tweet, component by component, from the client to
the home timelines of the followers.

REQUIRED: the Write API, the user's own timeline in SQL, the Fan Out Service,
the User Graph Service, one insert per follower into the Memory Cache, the
asynchronous work over a queue. Building the home timeline with a SQL join at
read time is the fail.

## Answer
