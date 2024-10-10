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

def load_query(query_file_path):
    """
    Load SQL query from a file.

    """
    with open(query_file_path, 'r') as file:
        query = file.read()
    return query

def run_query(query_file, output_csv=None):
    query = load_query(query_file)

    conn = sqlite3.connect(":memory:")

    # infection = pd.read_csv(comorbidity_code_path)
    infection_df = pd.read_csv(os.path.join(comorbidity_code_path, 'sepsis', 'infection.csv'))
    organ_dysfunction_df = pd.read_csv(os.path.join(comorbidity_code_path, 'sepsis', 'organ_dysfunction.csv'))
    explicit_sepsis_df = pd.read_csv(os.path.join(comorbidity_code_path, 'sepsis', 'explicit_sepsis.csv'))
    vent_df = pd.read_csv(os.path.join(comorbidity_code_path, 'sepsis', 'vent.csv'))
    admission = pd.read_csv(os.path.join(mimic_path,'hosp/admissions.csv'))
    diagnoses = pd.read_csv(os.path.join(mimic_path,'hosp/diagnoses_icd.csv'))
    procedure = pd.read_csv(os.path.join(mimic_path,'hosp/procedures_icd.csv'))

    infection_df.to_sql('infection', conn, if_exists='replace', index=False)
    organ_dysfunction_df.to_sql('organ', conn, if_exists='replace', index=False)
    explicit_sepsis_df.to_sql('esepsis', conn, if_exists='replace', index=False)
    vent_df.to_sql('vent', conn, if_exists='replace', index=False)
    admission.to_sql('admission', conn, if_exists='replace', index=False)
    diagnoses.to_sql('diagnoses', conn, if_exists='replace', index=False)
    procedure.to_sql('procedure', conn, if_exists='replace', index=False)

    start_time = time.time()
    result_df = pd.read_sql_query(query, conn)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken: {execution_time:.4f} seconds")

    if output_csv:
        result_df.to_csv(output_csv, index=False)

    conn.close()

    return result_df


if __name__ == "__main__":
    query_file = COM_QUERIES_DIR / 'sepsis_query.sql'
    
    output_csv = COM_RESULTS_DIR / 'sepsis_patients.csv'

    result_df = run_query(query_file, output_csv)
    print(f"Result saved to {output_csv}")
    print(result_df)
