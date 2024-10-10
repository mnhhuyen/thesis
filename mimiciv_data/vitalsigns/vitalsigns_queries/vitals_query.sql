WITH NonNullValues AS (
  SELECT
    tp.subject_id,
    tp.hadm_id,
    tp.stay_id,
    tp.intime,
    tp.outtime,
    vs.itemid,  -- Include vs.itemid to be accessible in the outer query
    CASE 
      WHEN vs.itemid = 223762 THEN vs.charttime -- Celsius
      WHEN vs.itemid = 223761 THEN vs.charttime -- Fahrenheit
      ELSE NULL 
    END AS temperature_charttime,

    -- Temperature (converted to Celsius if necessary)
    CASE 
      WHEN vs.itemid = 223762 THEN vs.value -- Celsius
      WHEN vs.itemid = 223761 THEN (vs.value - 32) / 1.8 -- Convert Fahrenheit to Celsius
      ELSE NULL 
    END AS temperature,

    -- Heart rate
    CASE 
      WHEN vs.itemid = 220045 THEN vs.charttime
      ELSE NULL 
    END AS hr_charttime,
    
    CASE WHEN vs.itemid = 220045 THEN vs.value ELSE NULL END AS heartrate,
    
    -- Aortic Pressure Signal - Diastolic
    CASE 
      WHEN vs.itemid = 228151 THEN vs.charttime
      ELSE NULL 
    END AS apd_charttime,
    
    CASE WHEN vs.itemid = 228151 THEN vs.value ELSE NULL END AS aorticpressure_dias,

    AVG(CASE WHEN vs.itemid = 228151 THEN vs.valuenum ELSE NULL END)
    OVER (PARTITION BY tp.stay_id) AS mean_aorticpressure_dias,

    -- Aortic Pressure Signal - Systolic
    CASE 
      WHEN vs.itemid = 228152 THEN vs.charttime
      ELSE NULL 
    END AS aps_charttime,
    
    CASE WHEN vs.itemid = 228152 THEN vs.value ELSE NULL END AS aorticpressure_sys,

    AVG(CASE WHEN vs.itemid = 228152 THEN vs.valuenum ELSE NULL END)
    OVER (PARTITION BY tp.stay_id) AS mean_aorticpressure_sys,

    -- Respiratory Rate
    CASE 
      WHEN vs.itemid IN (220210, 224690) THEN vs.charttime
      ELSE NULL 
    END AS rr_charttime,
    
    CASE WHEN vs.itemid IN (220210, 224690) THEN vs.value ELSE NULL END AS RespRate
  FROM vitalsigns vs
  JOIN target_patients tp 
    ON vs.subject_id = tp.subject_id
    AND vs.hadm_id = tp.hadm_id
    AND vs.stay_id = tp.stay_id

  -- Filter by the relevant vital sign item IDs
  WHERE vs.itemid IN (
    223761, -- Temperature F
    223762, -- Temperature C
    220045, -- Heart Rate
    228151, -- Aortic Pressure Signal - Diastolic
    228152, -- Aortic Pressure Signal - Systolic
    220210, -- Respiratory Rate
    224690  -- Respiratory Rate (Total)
  ) AND vs.value IS NOT NULL
), rn_values AS (
SELECT *,
       -- Row number for last non-null temperature within 24 hours
       ROW_NUMBER() OVER (
         PARTITION BY subject_id, hadm_id, stay_id
         ORDER BY CASE 
                   WHEN itemid IN (223761, 223762) 
                   AND temperature IS NOT NULL 
                   AND temperature_charttime >= intime 
                   AND temperature_charttime <= DATETIME(intime, '+1 day') 
                   THEN temperature_charttime 
                   ELSE NULL 
                 END DESC
       ) AS temp_row_num_last_24h,

       -- Row number for first non-null temperature within 10 days
       ROW_NUMBER() OVER (
         PARTITION BY subject_id, hadm_id, stay_id
         ORDER BY CASE 
                   WHEN itemid IN (223761, 223762) 
                   AND temperature IS NOT NULL 
                   AND temperature_charttime >= intime 
                   AND temperature_charttime <= DATETIME(intime, '+15 day') 
                   THEN temperature_charttime 
                   ELSE NULL 
                 END ASC
       ) AS temp_row_num_first_10d,

       -- Row number for last non-null heart rate within 24 hours
       ROW_NUMBER() OVER (
         PARTITION BY subject_id, hadm_id, stay_id
         ORDER BY CASE 
                   WHEN itemid = 220045 
                   AND heartrate IS NOT NULL 
                   AND hr_charttime >= intime 
                   AND hr_charttime <= DATETIME(intime, '+1 day') 
                   THEN hr_charttime 
                   ELSE NULL 
                 END DESC
       ) AS hr_row_num_last_24h,

       -- Row number for first non-null heart rate within 10 days
       ROW_NUMBER() OVER (
         PARTITION BY subject_id, hadm_id, stay_id
         ORDER BY CASE 
                   WHEN itemid = 220045 
                   AND heartrate IS NOT NULL 
                   AND hr_charttime >= intime 
                   AND hr_charttime <= DATETIME(intime, '+15 day') 
                   THEN hr_charttime 
                   ELSE NULL 
                 END ASC
       ) AS hr_row_num_first_10d,

       -- Row number for last non-null Aortic Pressure Diastolic within 24 hours
ROW_NUMBER() OVER (
  PARTITION BY subject_id, hadm_id, stay_id
  ORDER BY CASE 
            WHEN itemid = 228151  -- Diastolic
            AND aorticpressure_dias IS NOT NULL 
            AND apd_charttime >= intime 
            AND apd_charttime <= DATETIME(intime, '+1 day') 
            THEN apd_charttime 
            ELSE NULL 
          END DESC
) AS aortic_dias_row_num_last_24h,

-- Row number for first non-null Aortic Pressure Diastolic within 10 days
ROW_NUMBER() OVER (
  PARTITION BY subject_id, hadm_id, stay_id
  ORDER BY CASE 
            WHEN itemid = 228151  -- Diastolic
            AND aorticpressure_dias IS NOT NULL 
            AND apd_charttime >= intime 
            AND apd_charttime <= DATETIME(intime, '+15 day') 
            THEN apd_charttime 
            ELSE NULL 
          END ASC
) AS aortic_dias_row_num_first_10d,

-- Row number for last non-null Aortic Pressure Systolic within 24 hours
ROW_NUMBER() OVER (
  PARTITION BY subject_id, hadm_id, stay_id
  ORDER BY CASE 
            WHEN itemid = 228152  -- Systolic
            AND aorticpressure_sys IS NOT NULL 
            AND aps_charttime >= intime 
            AND aps_charttime <= DATETIME(intime, '+1 day') 
            THEN aps_charttime 
            ELSE NULL 
          END DESC
) AS aortic_sys_row_num_last_24h,

-- Row number for first non-null Aortic Pressure Systolic within 10 days
ROW_NUMBER() OVER (
  PARTITION BY subject_id, hadm_id, stay_id
  ORDER BY CASE 
            WHEN itemid = 228152  -- Systolic
            AND aorticpressure_sys IS NOT NULL 
            AND aps_charttime >= intime 
            AND aps_charttime <= DATETIME(intime, '+15 day') 
            THEN aps_charttime 
            ELSE NULL 
          END ASC
) AS aortic_sys_row_num_first_10d,

-- Row number for last non-null Respiratory Rate within 24 hours
ROW_NUMBER() OVER (
  PARTITION BY subject_id, hadm_id, stay_id
  ORDER BY CASE 
            WHEN itemid IN (220210, 224690)  -- Respiratory Rate
            AND RespRate IS NOT NULL 
            AND rr_charttime >= intime 
            AND rr_charttime <= DATETIME(intime, '+1 day') 
            THEN rr_charttime 
            ELSE NULL 
          END DESC
) AS resp_row_num_last_24h,

-- Row number for first non-null Respiratory Rate within 10 days
ROW_NUMBER() OVER (
  PARTITION BY subject_id, hadm_id, stay_id
  ORDER BY CASE 
            WHEN itemid IN (220210, 224690)  -- Respiratory Rate
            AND RespRate IS NOT NULL 
            AND rr_charttime >= intime 
            AND rr_charttime <= DATETIME(intime, '+15 day') 
            THEN rr_charttime 
            ELSE NULL 
          END ASC
) AS resp_row_num_first_10d

FROM NonNullValues
)
SELECT
  subject_id,
  hadm_id,
  stay_id,
  intime,
  outtime,
  
  -- Coalesce to return the last non-null value within 24h or the first available non-null one within 10 days for each column
  COALESCE(
    MAX(CASE WHEN temp_row_num_last_24h = 1 THEN temperature END),
    MAX(CASE WHEN temp_row_num_first_10d = 1 THEN temperature END)
  ) AS temperature,

  COALESCE(
    MAX(CASE WHEN hr_row_num_last_24h = 1 THEN heartrate END),
    MAX(CASE WHEN hr_row_num_first_10d = 1 THEN heartrate END)
  ) AS heart_rate,

  COALESCE(
    MAX(CASE WHEN aortic_dias_row_num_last_24h = 1 THEN aorticpressure_dias END),
    MAX(CASE WHEN aortic_dias_row_num_first_10d = 1 THEN aorticpressure_dias END)
  ) AS aorticpressure_dias,

  COALESCE(
    MAX(CASE WHEN aortic_sys_row_num_last_24h = 1 THEN aorticpressure_sys END),
    MAX(CASE WHEN aortic_sys_row_num_first_10d = 1 THEN aorticpressure_sys END)
  ) AS aorticpressure_sys,

  COALESCE(
    MAX(CASE WHEN resp_row_num_last_24h = 1 THEN RespRate END),
    MAX(CASE WHEN resp_row_num_first_10d = 1 THEN RespRate END)
  ) AS resp_rate,

  -- Include the mean values for Aortic Pressure Diastolic and Systolic
  MAX(mean_aorticpressure_dias) AS mean_aorticpressure_dias,
  MAX(mean_aorticpressure_sys) AS mean_aorticpressure_sys

FROM rn_values
GROUP BY subject_id, hadm_id, stay_id
ORDER BY subject_id, hadm_id, stay_id;