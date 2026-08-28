-- QUERY: Reps Per Node, Zeros Kept
-- TRAINS: sql-join-left-keep
--
-- Tables:
--
--     nodes
--         id     TEXT
--         name   TEXT
--         group  TEXT
--         added  TEXT
--         desc   TEXT
--         hint   TEXT
--         drill  TEXT
--
--     verdicts
--         file     TEXT
--         node_id  TEXT
--         verdict  TEXT
--
-- Return every node in the graph with how many verdicts it has. A node with
-- no verdicts must still appear, with 0.
-- Columns: node_id, reps.
--
-- REQUIRED: a LEFT JOIN with the count taken on the right-hand column, so the
-- unmatched rows count 0 and not 1. COUNT(*) is the failure mode this kills.

select n.id, count(v.verdict) as reps
    from nodes as n
    left join verdicts as v on v.node_id = n.id
    group by n.id;