import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path
import time

sys.path.append(str(Path(__file__).resolve().parent.parent))

from demographics_runs import DEMO_QUERIES_DIR, DEMO_RESULTS_DIR
from config.config_param import mimic_path, derive_path, target_patients_path

def load_query(query_file_path):
    """
    Load SQL query from a file.
    """
    with open(query_file_path, 'r') as file:
        query = file.read()
    return query

def run_query_sqlite(query_file, output_csv=None):
    query = load_query(query_file)

    conn = sqlite3.connect(":memory:")  

    target_patients = pd.read_csv(target_patients_path)
    gcs_csv_path = os.path.join(derive_path, 'gcs.csv')  
    gcs_df = pd.read_csv(gcs_csv_path)

    target_patients.to_sql('target_patients', conn, index=False, if_exists='replace')
    gcs_df.to_sql('gcs', conn, index=False, if_exists='replace')

    start_time = time.time()
    result_df = pd.read_sql_query(query, conn)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken with SQLite: {execution_time:.4f} seconds")

    if output_csv:
        result_df.to_csv(output_csv, index=False)
        print(f"Result saved to {output_csv}")

    conn.close()

    return result_df

if __name__ == "__main__":
    query_file = DEMO_QUERIES_DIR / 'gcs_query.sql'
    output_csv = DEMO_RESULTS_DIR / 'gcs_output.csv'

    result_df = run_query_sqlite(query_file, output_csv)
    print(result_df)
