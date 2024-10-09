SELECT
    tp.subject_id,
    tp.stay_id,
    MIN(CASE WHEN bg.specimen = 'ART.' THEN po2 END) AS pao2_min,
    MAX(CASE WHEN bg.specimen = 'ART.' THEN po2 END) AS pao2_max,
    MIN(CASE WHEN bg.specimen = 'ART.' THEN pco2 END) AS pco2_min,
    MAX(CASE WHEN bg.specimen = 'ART.' THEN pco2 END) AS pco2_max,
    MIN(spo2) AS spo2_min, MAX(spo2) AS spo2_max,
    MIN(pao2fio2ratio) AS pao2fio2ratio_min, MAX(pao2fio2ratio) AS pao2fio2ratio_max,
    MIN(totalco2) AS totalco2_min, MAX(totalco2) AS totalco2_max,
    MIN(aniongap) AS aniongap_min, MAX(aniongap) AS aniongap_max,
    MIN(bicarbonate) AS bicarbonate_min, MAX(bicarbonate) AS bicarbonate_max,
    MIN(baseexcess) AS baseexcess_min, MAX(baseexcess) AS baseexcess_max,
    MIN(ph) AS ph_min, MAX(ph) AS ph_max
FROM target_patients tp
LEFT JOIN bloodgas bg
    ON tp.subject_id = bg.subject_id
    AND bg.charttime >= DATETIME(tp.intime, '-1 day')
    AND bg.charttime <= DATETIME(tp.intime, '+7 day')
GROUP BY tp.subject_id, tp.stay_id;
