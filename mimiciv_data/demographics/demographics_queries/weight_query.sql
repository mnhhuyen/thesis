SELECT
    tp.subject_id
    , tp.stay_id
    , AVG(
        CASE WHEN weight_type = 'admit' THEN ce.weight ELSE NULL END
    ) AS weight_admit
    , AVG(ce.weight) AS weight
    , MIN(ce.weight) AS weight_min
    , MAX(ce.weight) AS weight_max
FROM target_patients tp
-- admission weight
LEFT JOIN weight_durations ce
    ON tp.stay_id = ce.stay_id
        -- we filter to weights documented during or before the 1st day
        AND ce.starttime <= DATETIME(tp.intime, '+1 DAY')
GROUP BY tp.subject_id, tp.stay_id
;