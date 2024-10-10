import os
import sys
import pandas as pd
import pandasql as psql
from pathlib import Path
import time
import sqlite3

sys.path.append(str(Path(__file__).resolve().parent.parent))

from demographics_runs import DEMO_QUERIES_DIR, DEMO_RESULTS_DIR
from config.config_param import mimic_path, derive_path, target_patients_path

def load_query(query_file_path):
    with open(query_file_path, 'r') as file:
        query = file.read()
    return query

def run_query(query_file, output_csv=None):
    query = load_query(query_file)

    conn = sqlite3.connect(":memory:")

    target_patients = pd.read_csv(target_patients_path)
    mv_duration = pd.read_csv(os.path.join(derive_path, 'ventilation_durations.csv'))
    # procedureevents_mv = pd.read_csv(os.path.join(mimic_path, 'icu/procedureevents.csv'))

    target_patients.to_sql('target_patients', conn, index=False, if_exists='replace')
    mv_duration.to_sql('mv_duration', conn, index=False, if_exists='replace')
    # procedureevents_mv.to_sql('procedureevents_mv', conn, index=False, if_exists='replace')

    start_time = time.time()
    result_df = pd.read_sql_query(query, conn)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken using SQLite directly: {execution_time:.4f} seconds")

    if output_csv:
        result_df.to_csv(output_csv, index=False)

    conn.close()

    return result_df

if __name__ == "__main__":
    query_file = DEMO_QUERIES_DIR / 'duration_mv_query.sql'
    output_csv = DEMO_RESULTS_DIR / 'duration_mv_output.csv'

    result_df = run_query(query_file, output_csv)
    print(f"Result saved to {output_csv}")
    print(result_df)
