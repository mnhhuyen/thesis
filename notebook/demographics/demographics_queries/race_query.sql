SELECT
    tp.subject_id, tp.hadm_id, tp.stay_id,
    a.race
FROM target_patients tp
LEFT JOIN admissions a ON tp.subject_id = a.subject_id
GROUP BY tp.subject_id, tp.stay_id
