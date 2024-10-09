import os
import sys
import pandas as pd
import sqlite3
import time
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

from comorbidity_runs import COM_RESULTS_DIR
from config.config_param import mimic_path, target_patients_path, comorbidity_code_path

### have to run sepsis.py first

# list of disease files
list_disease_path = [file for file in os.listdir(comorbidity_code_path) if file.endswith('.csv')]
comorbidity_files = {os.path.splitext(file)[0]: os.path.join(comorbidity_code_path, file) for file in list_disease_path}

conn = sqlite3.connect(':memory:')  

diagnoses = pd.read_csv(os.path.join(mimic_path, 'hosp/diagnoses_icd.csv'))
target_patients = pd.read_csv(target_patients_path)
sepsis = pd.read_csv(COM_RESULTS_DIR / 'sepsis_patients.csv')

# merge target_patients with sepsis data
# since with sepsis, we have a total sepsis patients file. So we just need to join 2 table
target_patients = pd.merge(target_patients, sepsis[['subject_id', 'sepsis']], on='subject_id', how='left')
target_patients['sepsis'] = target_patients['sepsis'].fillna(0).astype(int)  

#write df to sqlite database (conn)
diagnoses.to_sql('diagnoses', conn, index=False, if_exists='replace')
target_patients.to_sql('target_patients', conn, index=False, if_exists='replace')

# load table to conn 
# combine the query for each comorbidity table
def load_comorbidity_table(conn, disease_name, disease_file):
    disease_df = pd.read_csv(disease_file)
    disease_df.to_sql(disease_name, conn, index=False, if_exists='replace')
    
    query = f"""
    MAX(CASE
        WHEN d.icd_code IN (SELECT icd_code FROM {disease_name}) THEN 1
        ELSE 0
    END) AS {disease_name}
    """
    return query

start_time = time.time()

# start building the combined query
combined_query = """
SELECT tp.subject_id, tp.hadm_id, tp.stay_id, tp.sepsis
"""

# iterate through comorbidity files and append the CASE statements
for disease_name, disease_file in comorbidity_files.items():
    condition_query = load_comorbidity_table(conn, disease_name, disease_file)
    combined_query += f", {condition_query}"

# complete the query
combined_query += """
FROM target_patients tp
LEFT JOIN diagnoses d ON tp.subject_id = d.subject_id AND tp.hadm_id = d.hadm_id
GROUP BY tp.subject_id, tp.hadm_id, tp.stay_id, tp.sepsis;
"""


result_df = pd.read_sql_query(combined_query, conn)

end_time = time.time()
execution_time = end_time - start_time
print(f"Time taken: {execution_time:.4f} seconds")

output_file = Path(COM_RESULTS_DIR) / 'patients_with_comorbidity.csv'
result_df.to_csv(output_file, index=False)

print(f"Comorbidity results saved to {output_file}")


conn.close()
