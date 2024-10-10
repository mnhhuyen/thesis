import pandas as pd
from config.config_param import target_patients_path, sorted_data_path, final_data_path
import os
import numpy as np

target_patients = pd.read_csv(target_patients_path)
gender = pd.read_csv(os.path.join(sorted_data_path, 'gender_output.csv'))
race = pd.read_csv(os.path.join(sorted_data_path, 'race_output.csv'))
# height = pd.read_csv(os.path.join(sorted_data_path, 'height_output.csv'))
# weight = pd.read_csv(os.path.join(sorted_data_path, 'weight_output.csv'))
bmi = pd.read_csv(os.path.join(sorted_data_path, 'bmi_output.csv'))
gcs = pd.read_csv(os.path.join(sorted_data_path, 'gcs_output.csv'))
duration = pd.read_csv(os.path.join(sorted_data_path, 'duration_mv_output.csv'))
vitalsigns = pd.read_csv(os.path.join(sorted_data_path, 'vitalsign_output.csv'))
urine_output = pd.read_csv(os.path.join(sorted_data_path, 'urine_output_output.csv'))
bg = pd.read_csv(os.path.join(sorted_data_path, 'bg_output.csv'))
lab = pd.read_csv(os.path.join(sorted_data_path, 'lab_output.csv'))
comor = pd.read_csv(os.path.join(sorted_data_path, 'patients_with_comorbidity.csv'))
score = pd.read_csv(os.path.join(sorted_data_path, 'score_output.csv'))


target_patients['gender'] = gender['gender']
target_patients['race'] = race['race']
# target_patients['height'] = height['height']
# target_patients['weight'] = np.where(weight['weight_admit'].isna(), 
#                                      weight['weight'],
#                                      weight['weight_admit'])
target_patients['bmi'] = bmi['bmi']
target_patients['gcs'] = gcs['gcs_min']
target_patients['gcs_unable'] = gcs['gcs_unable']
target_patients['mv_duration'] = duration['duration']
target_patients['temperature'] = vitalsigns['temperature_mean']
target_patients['heart_rate'] = vitalsigns['heart_rate_mean']
target_patients['map_dias'] = vitalsigns['map_dias_mean']
target_patients['map_sys'] = vitalsigns['map_sys_mean']
target_patients['respiratory_rate'] = vitalsigns['resp_rate_mean']
target_patients['urine_output'] = urine_output['urineoutput']
# target_patients['pao2'] = (bg['pao2_min'] + bg['pao2_max']) / 2
# target_patients['paco2'] = (bg['pco2_min'] + bg['pco2_max']) / 2
# target_patients['spo2'] = (bg['spo2_min'] + bg['spo2_max']) / 2
# target_patients['pfr'] = (bg['pao2fio2ratio_min'] + bg['pao2fio2ratio_max']) / 2
# target_patients['pfr'] = (bg['pao2fio2ratio_min'] + bg['pao2fio2ratio_max']) / 2
# target_patients['total_co2'] = (bg['totalco2_min'] + bg['totalco2_max']) / 2
# target_patients['anion_gap'] = (bg['aniongap_min'] + bg['aniongap_max']) / 2
# target_patients['bicarbonate'] = (bg['bicarbonate_min'] + bg['bicarbonate_max']) / 2
# target_patients['base_excess'] = (bg['baseexcess_min'] + bg['baseexcess_max']) / 2
# target_patients['ph'] = (bg['ph_min'] + bg['ph_max']) / 2
# target_patients['wbc'] = (lab['wbc_min'] + lab['wbc_max']) / 2
# target_patients['rbc'] = (lab['rbc_min'] + lab['rbc_max']) / 2
# target_patients['plt'] = (lab['platelets_min'] + lab['platelets_max']) / 2
# target_patients['hemoglobin'] = (lab['hemoglobin_min'] + lab['hemoglobin_max']) / 2

bg_columns = ['pao2','pco2','spo2','pao2fio2ratio', 'totalco2', 'aniongap', 'bicarbonate', 'baseexcess', 'ph']
lab_columns = ['wbc', 'rbc', 'platelets', 'hemoglobin', 'hematocrit', 'creatinine', 'bun', 'alt', 'ast',
               'lactate', 'glucose', 'sodium', 'potassium', 'calcium', 'magnesium', 'chloride',
               'ck', 'ck_mb', 'ntprobnp', 'troponin_t', 'inr', 'pt']

comor_columns = ['sepsis', 'anemia', 'ami', 'ventricular_arrhythmia', 'diabetes', 'valvular_disease',
                 'ckd', 'pneumonia', 'copd', 'atrial_fibrillation', 'aki', 'angina_pectoris',
                 'liver_cirrhosis', 'pleural_effusion', 'omi', 'hypertension', 'hepatitis', 'stroke', 'pe']

for col in bg_columns:
    target_patients[col] = (bg[f'{col}_min'] + bg[f'{col}_max']) / 2

for col in lab_columns:
    target_patients[col] = (lab[f'{col}_min'] + lab[f'{col}_max']) / 2

for col in comor_columns:
    target_patients[col] = comor[col]

target_patients['sofa'] = score['sofa_24hours']
target_patients['sapsii'] = score['sapsii']
target_patients['lods'] = score['lods']

target_patients.to_csv(final_data_path, index=False)
