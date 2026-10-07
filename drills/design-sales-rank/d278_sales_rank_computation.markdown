DRILL: Sales Rank Computation
TRAINS: design-sales-rank

Design the feature that shows the past week's most popular products by
category. Assume 10 million products, 1000 categories, 1 billion transactions
per month, 100 billion read requests per month, results updated hourly, and 40
bytes per transaction.

Write the two steps of the computation and say where its result goes.

REQUIRED: the MapReduce to (category, product_id) with the summed quantity,
the distributed sort, the sales_rank table with its indexes. Computing the
rank with a query per page view is the fail.

## Answer
