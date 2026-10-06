DRILL: Twitter Timeline
TRAINS: design-twitter-timeline

Design the Twitter timeline. A user posts a tweet; a user views the home
timeline, the tweets of the people they follow; a user views their own
timeline; a user searches keywords. Assume 100 million active users, 500
million tweets per day, an average fanout of 10 deliveries per tweet, 250
billion read requests and 10 billion searches per month. Write: (1) tweets
per second, fanout deliveries per second, reads per second, searches per
second; (2) the path of posting a tweet, with where the user's own tweets
and where the home timelines are stored, and why; (3) the path of reading
the home timeline; (4) the bottleneck of the fan out and two ways to
mitigate it; (5) two measures that bound the memory used.

REQUIRED: four rates, the fan out on write into a memory cache with the
reason, the read path with its multigets, the highly-followed user, two
memory bounds. Building the home timeline with a SQL join at read time is
the fail.

## Answer
