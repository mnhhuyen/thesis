SELECT tp.subject_id, tp.hadm_id, tp.stay_id, l.lods
FROM target_patients tp
LEFT JOIN lods l
ON tp.stay_id = l.stay_id
GROUP BY tp.stay_id
