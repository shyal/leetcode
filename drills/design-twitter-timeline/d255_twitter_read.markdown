Design the Twitter timeline. A user posts a tweet; a user views the home
timeline, the tweets of the people they follow; a user views their own
timeline; a user searches keywords. Assume 100 million active users, 500
million tweets per day, an average fanout of 10 deliveries per tweet, 250
billion read requests and 10 billion searches per month.

Write the path of reading the home timeline, component by component, with the
cost of each step.

REQUIRED: the Read API, the Timeline Service, the O(1) read of ids from the
Memory Cache, the O(n) multigets of tweet and user info. Fetching each tweet
with its own request is the fail.

## Answer
