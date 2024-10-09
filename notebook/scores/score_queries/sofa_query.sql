SELECT tp.subject_id, tp.hadm_id, tp.stay_id, sf.sofa_24hours
FROM target_patients tp
JOIN sofa sf
ON tp.stay_id = sf.stay_id
    AND sf.starttime >= DATETIME(tp.intime, '-6 hour')
    AND sf.starttime <= DATETIME(tp.intime, '+1 day')
GROUP BY tp.stay_id
