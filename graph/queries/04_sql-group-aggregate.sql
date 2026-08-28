-- QUERY: Reps Per Node
-- TRAINS: sql-group-aggregate
--
-- Tables:
--
--     verdicts
--         file     TEXT
--         node_id  TEXT
--         verdict  TEXT
--
-- Return every node that has a verdict, with how many verdicts it has
-- collected, most-drilled first.
-- Columns: node_id, reps.
--
-- REQUIRED: one GROUP BY. NO subquery per node.

select node_id, count(verdict)
    from verdicts
    group by node_id
    order by count(verdict);
