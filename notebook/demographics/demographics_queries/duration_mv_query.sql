SELECT tp.subject_id, tp.hadm_id, tp.stay_id, sum(mv.duration_hours) as duration
FROM target_patients tp
LEFT JOIN mv_duration mv
ON tp.stay_id = mv.stay_id
    AND ((mv.starttime >= DATETIME(tp.intime, '-6 hour') AND mv.starttime <= DATETIME(tp.intime, '+1 day')) 
        OR (mv.starttime <= tp.intime AND mv.endtime >= tp.intime))
GROUP BY tp.stay_id