DRILL: Sales Rank
TRAINS: design-sales-rank

Design the feature that shows the past week's most popular products by
category. Assume 10 million products, 1000 categories, 1 billion
transactions per month, 100 billion read requests per month, results updated
hourly, and 40 bytes per transaction. Write: (1) transactions per second,
reads per second and new content per month; (2) where the raw sales data is
stored; (3) the two steps of the computation and where its result goes; (4)
the read path; (5) what handles the read load and what is done about the
write load.

REQUIRED: three numbers, the logs in an object store, the two MapReduce
steps into the sales_rank table, the read path, the cache and the SQL
scaling. Computing the rank with a query per page view is the fail.

## Answer
