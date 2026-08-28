-- QUERY: Clean And Struggled Per Node
-- TRAINS: sql-conditional-aggregate
--
-- Tables:
--
--     verdicts
--         file     TEXT
--         node_id  TEXT
--         verdict  TEXT
--
-- Return one row per node with a verdict: the clean and struggled counts as
-- two columns.
-- Columns: node_id, clean, struggled.
--
-- REQUIRED: one GROUP BY; each count comes from a CASE inside the aggregate.
-- Two joins or two subqueries is the failure mode this kills.

select node_id,
    sum(case when verdict = 'clean'         then 1 else 0 end) as clean,
    sum(case when verdict = 'struggled'     then 1 else 0 end) as struggled
    from verdicts
    group by node_id;
