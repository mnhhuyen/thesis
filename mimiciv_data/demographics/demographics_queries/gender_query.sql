SELECT
    tp.subject_id, tp.hadm_id, tp.stay_id,
    p.gender
FROM target_patients tp
LEFT JOIN patients p ON tp.subject_id = p.subject_id
GROUP BY tp.subject_id, tp.stay_id;