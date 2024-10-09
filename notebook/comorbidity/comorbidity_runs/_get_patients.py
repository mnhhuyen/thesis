import os
import sys
import pandas as pd
import pandasql as psql
from pathlib import Path
import time
import sqlite3

sys.path.append(str(Path(__file__).resolve().parent.parent))

from comorbidity_runs import COM_QUERIES_DIR, COM_RESULTS_DIR
from config.config_param import mimic_path, derive_path, target_patients_path, comorbidity_code_path


diagnoses = pd.read_csv(os.path.join(mimic_path,'hosp/diagnoses_icd.csv'))

list_disease_path = [os.path.join(comorbidity_code_path, file) for file in os.listdir(comorbidity_code_path) if file.endswith('.csv')]

def load_patients(disease_path):
    disease_data = pd.read_csv(disease_path)
    disease_codes = disease_data['icd_code'].tolist()
    disease_patients = diagnoses[diagnoses['icd_code'].isin(disease_codes)]

    disease_name = os.path.splitext(os.path.basename(disease_path))[0]
    output_file = os.path.join(COM_RESULTS_DIR, f'{disease_name}_patients.csv')
    disease_patients.to_csv(output_file, index=False)
    print(f'Saved patients for {disease_name} to {output_file}')



for disease_path in list_disease_path:
    load_patients(disease_path)
