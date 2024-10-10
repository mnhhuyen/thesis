SELECT
    tp.subject_id
    , tp.stay_id
    , ROUND(CAST(AVG(height) AS NUMERIC), 2) AS height
FROM target_patients tp
LEFT JOIN height ht
    ON tp.stay_id = ht.stay_id
        AND ht.charttime >= DATETIME(tp.intime, '-6 HOUR')
        AND ht.charttime <= DATETIME(tp.intime, '+1 DAY')
GROUP BY tp.subject_id, tp.stay_id;