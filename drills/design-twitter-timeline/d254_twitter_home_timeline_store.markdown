DRILL: Twitter Home Timeline Store
TRAINS: design-twitter-timeline

Design the Twitter timeline. A user posts a tweet; a user views the home
timeline, the tweets of the people they follow; a user views their own
timeline; a user searches keywords. Assume 100 million active users, 500
million tweets per day, an average fanout of 10 deliveries per tweet, 250
billion read requests and 10 billion searches per month.

Say where the home timelines are stored and why that store, and where a user's
own timeline is stored.

REQUIRED: the Memory Cache, a Redis list, chosen for its write rate; the own
timeline in SQL. Putting the home timelines in the relational database is the
fail.

## Answer
