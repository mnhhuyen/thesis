WITH gcs_final AS (
    SELECT
        tp.subject_id, tp.stay_id
        , g.gcs
        , g.gcs_motor
        , g.gcs_verbal
        , g.gcs_eyes
        , g.gcs_unable
        -- This sorts the data by GCS
        -- rn = 1 is the the lowest total GCS value
        , ROW_NUMBER() OVER
        (
            PARTITION BY g.stay_id
            ORDER BY g.gcs
        ) AS gcs_seq
    FROM target_patients tp
    -- Only get data for the first 24 hours
    LEFT JOIN gcs g
        ON tp.stay_id = g.stay_id
            AND g.charttime >= DATETIME(tp.intime, '-6 HOUR')
            AND g.charttime <= DATETIME(tp.intime, '+1 DAY')
)

SELECT
    tp.subject_id
    , tp.stay_id
    -- The minimum GCS is determined by the above row partition
    -- we only join if gcs_seq = 1
    , gcs AS gcs_min
    , gcs_motor
    , gcs_verbal
    , gcs_eyes
    , gcs_unable
FROM target_patients tp
LEFT JOIN gcs_final gs
    ON tp.stay_id = gs.stay_id
        AND gs.gcs_seq = 1
;