import os
import sys
import pandas as pd
import pandasql as psql
from pathlib import Path
import time
import sqlite3

sys.path.append(str(Path(__file__).resolve().parent.parent))

from lab_runs import LAB_QUERIES_DIR, LAB_RESULTS_DIR
from config.config_param import mimic_path, derive_path, target_patients_path

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

    target_patients = pd.read_csv(target_patients_path)
    blood_count = pd.read_csv(os.path.join(derive_path, 'blood_count.csv'))
    chemistry = pd.read_csv(os.path.join(derive_path, 'chemistry.csv'))
    coagulation = pd.read_csv(os.path.join(derive_path, 'coagulation.csv'))
    enzymes = pd.read_csv(os.path.join(derive_path, 'enzyme.csv'))
    cardiac_marker = pd.read_csv(os.path.join(derive_path, 'cardiac_marker.csv'))

    target_patients.to_sql('target_patients', conn, index=False, if_exists='replace')
    blood_count.to_sql('blood_count', conn, index=False, if_exists='replace')
    chemistry.to_sql('chemistry', conn, index=False, if_exists='replace')
    coagulation.to_sql('coagulation', conn, index=False, if_exists='replace')
    enzymes.to_sql('enzyme', conn, index=False, if_exists='replace')
    cardiac_marker.to_sql('cardiac_marker', conn, index=False, if_exists='replace')

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
    query_file = LAB_QUERIES_DIR / 'lab_query.sql'
    
    output_csv = LAB_RESULTS_DIR / 'lab_output.csv'

    result_df = run_query(query_file, output_csv)
    print(f"Result saved to {output_csv}")
    print(result_df)
