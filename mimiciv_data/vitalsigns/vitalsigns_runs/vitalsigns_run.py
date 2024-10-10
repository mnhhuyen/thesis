import os
import sys
import pandas as pd
# import pandasql as psql
from pathlib import Path
import time
import sqlite3

sys.path.append(str(Path(__file__).resolve().parent.parent))

from vitalsigns_runs import VITAL_QUERIES_DIR, VITAL_RESULTS_DIR
from config.config_param import mimic_path, derive_path, target_patients_path

def load_query(query_file_path):
    with open(query_file_path, 'r') as file:
        query = file.read()
    return query

def run_query(query_file, output_csv=None):
    query = load_query(query_file)

    conn = sqlite3.connect(":memory:")

    target_patients = pd.read_csv(target_patients_path)
    vitalsigns = pd.read_csv(os.path.join(derive_path, 'vitalsigns.csv'))

    target_patients.to_sql('target_patients', conn, index=False, if_exists='replace')
    vitalsigns.to_sql('vitalsigns', conn, index=False, if_exists='replace')

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
    query_file = VITAL_QUERIES_DIR / 'vitalsign_query.sql'
    output_csv = VITAL_RESULTS_DIR / 'vitalsign_output.csv'

    result_df = run_query(query_file, output_csv)
    print(f"Result saved to {output_csv}")
    print(result_df)
