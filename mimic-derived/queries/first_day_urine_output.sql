DROP TABLE IF EXISTS first_day_urine_output; CREATE TABLE first_day_urine_output AS
SELECT
  ie.subject_id,
  ie.stay_id,
  SUM(urineoutput) AS urineoutput
FROM icustays AS ie
LEFT JOIN urine_output AS uo
  ON ie.stay_id = uo.stay_id
  AND uo.charttime >= ie.intime
  AND uo.charttime <= ie.intime + INTERVAL '1' DAY
GROUP BY
  ie.subject_id,
  ie.stay_id