REFERENCE: d278 Sales Rank Computation
SOURCE: System Design Primer, "Design Amazon's sales rank by category feature" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md

REQUIRED
- MapReduce step 1: transform the data to (category, product_id),
  sum(quantity).
- MapReduce step 2: a distributed sort.
- The sorted result is inserted into an aggregate sales_rank table in a SQL
  Database, indexed on id, category_id and product_id.
