SELECT
    -- patient identifiers
    tp.subject_id
    , tp.stay_id
    , SUM(urineoutput) AS urineoutput
FROM target_patients tp
-- Join to the outputevents table to get urine output
LEFT JOIN urine_output uo
    ON tp.stay_id = uo.stay_id
        -- ensure the data occurs during the first day
        AND uo.charttime >= tp.intime
        AND uo.charttime <= DATETIME(tp.intime, '+1 DAY')
GROUP BY tp.subject_id, tp.stay_id