-- QUERY: Nodes That Fight Back
-- TRAINS: sql-having-filter-groups
--
-- Tables:
--
--     verdicts
--         file     TEXT
--         node_id  TEXT
--         verdict  TEXT
--
-- Return every node with at least 3 struggled verdicts.
-- Columns: node_id, struggles.
--
-- REQUIRED: the filter on the count goes in HAVING, not WHERE, and NOT in a
-- wrapping subquery.

select node_id, count(verdict) as strugles
    from verdicts
    where verdict = 'struggled'
    group by node_id
    having count(verdict) >= 3;