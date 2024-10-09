SELECT tp.subject_id, tp.hadm_id, tp.stay_id, ss.sapsii
FROM target_patients tp
JOIN sapsii ss
ON tp.stay_id = ss.stay_id
    AND ss.starttime >= DATETIME(tp.intime, '-6 hour')
    AND ss.starttime <= DATETIME(tp.intime, '+1 day')
GROUP BY tp.stay_id
