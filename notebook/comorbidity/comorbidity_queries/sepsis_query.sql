WITH infection_group AS
(
    SELECT diagnoses.*
    FROM diagnoses
    JOIN infection 
    ON diagnoses.icd_code = infection.icd_code
), 

organ_dysfunction_group AS
(
	SELECT diagnoses.*
    FROM diagnoses
    JOIN organ
    ON diagnoses.icd_code = organ.icd_code
),

explicit_sepsis_group AS
(
	SELECT diagnoses.*
    FROM diagnoses
    JOIN esepsis
    ON diagnoses.icd_code = esepsis.icd_code
),

vent_group AS
(
	SELECT procedure.*
    FROM procedure
    JOIN vent
    ON procedure.icd_code = vent.icd_code
),

aggregation AS
(
    SELECT 
        subject_id, hadm_id,
        CASE WHEN hadm_id IN (SELECT DISTINCT hadm_id FROM infection_group) THEN 1 ELSE 0 END AS infection,
        CASE WHEN hadm_id IN (SELECT DISTINCT hadm_id FROM explicit_sepsis_group) THEN 1 ELSE 0 END AS explicit_sepsis,
        CASE WHEN hadm_id IN (SELECT DISTINCT hadm_id FROM organ_dysfunction_group) THEN 1 ELSE 0 END AS organ_dysfunction,
        CASE WHEN hadm_id IN (SELECT DISTINCT hadm_id FROM vent_group) THEN 1 ELSE 0 END AS mech_vent
    FROM admission
),

compute AS
(
    SELECT subject_id, hadm_id, infection, explicit_sepsis, organ_dysfunction, mech_vent,
        CASE
            WHEN explicit_sepsis = 1 THEN 1
            WHEN infection = 1 AND organ_dysfunction = 1 THEN 1
            WHEN infection = 1 AND mech_vent = 1 THEN 1
            ELSE 0
        END AS sepsis
    FROM aggregation
)

SELECT subject_id, hadm_id, sepsis
FROM compute
WHERE sepsis = 1;
