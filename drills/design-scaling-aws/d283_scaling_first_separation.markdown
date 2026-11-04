Design a system that grows from one user to 10 million. Assume relational
data, 1 billion writes and 100 billion reads per month, and 1 KB per write.

Name the first two things moved off the single box, and why.

REQUIRED: static content to an object store, MySQL to its own box, independent
scaling. Moving the database last is the fail.

## Answer
