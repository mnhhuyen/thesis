WITH sf_score AS (
    SELECT tp.subject_id, tp.hadm_id, tp.stay_id, sf.sofa_24hours
    FROM target_patients tp
    JOIN sofa sf
    ON tp.stay_id = sf.stay_id
    AND ((sf.starttime >= DATETIME(tp.intime, '-6 hour') AND sf.starttime <= DATETIME(tp.intime, '+1 day')) 
        OR (sf.starttime <= tp.intime AND sf.endtime >= tp.intime))
    GROUP BY tp.stay_id
),
ss_score AS (
    SELECT tp.subject_id, tp.hadm_id, tp.stay_id, ss.sapsii
    FROM target_patients tp
    JOIN sapsii ss
    ON tp.stay_id = ss.stay_id
    AND ((ss.starttime >= DATETIME(tp.intime, '-6 hour') AND ss.starttime <= DATETIME(tp.intime, '+1 day')) 
        OR (ss.starttime <= tp.intime AND ss.endtime >= tp.intime))
    GROUP BY tp.stay_id
),
lods_score AS (
    SELECT tp.subject_id, tp.hadm_id, tp.stay_id, l.lods
    FROM target_patients tp
    JOIN lods l
    ON tp.stay_id = l.stay_id
    GROUP BY tp.stay_id
)

SELECT tp.subject_id, tp.hadm_id, tp.stay_id, 
       sf_score.sofa_24hours, 
       ss_score.sapsii, 
       lods_score.lods
FROM target_patients tp
LEFT JOIN sf_score ON tp.stay_id = sf_score.stay_id
LEFT JOIN ss_score ON tp.stay_id = ss_score.stay_id
LEFT JOIN lods_score ON tp.stay_id = lods_score.stay_id
GROUP BY tp.stay_id;
