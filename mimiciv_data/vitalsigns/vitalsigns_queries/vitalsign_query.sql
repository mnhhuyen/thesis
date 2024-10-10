SELECT
    tp.subject_id
    , tp.stay_id
    , MIN(heart_rate) AS heart_rate_min
    , MAX(heart_rate) AS heart_rate_max
    , AVG(heart_rate) AS heart_rate_mean
    , MIN(resp_rate) AS resp_rate_min
    , MAX(resp_rate) AS resp_rate_max
    , AVG(resp_rate) AS resp_rate_mean
    , MIN(temperature) AS temperature_min
    , MAX(temperature) AS temperature_max
    , AVG(temperature) AS temperature_mean
    , MIN(map_dias) AS map_dias_min
    , MAX(map_dias) AS map_dias_max
    , AVG(map_dias) AS map_dias_mean
    , MIN(map_sys) AS map_sys_min
    , MAX(map_sys) AS map_sys_max
    , AVG(map_sys) AS map_sys_mean
FROM target_patients tp
LEFT JOIN vitalsigns ce
    ON tp.stay_id = ce.stay_id
        AND ce.charttime >= DATETIME(tp.intime, '-6 HOUR')
        AND ce.charttime <= DATETIME(tp.intime, '+1 DAY')
GROUP BY tp.subject_id, tp.stay_id;