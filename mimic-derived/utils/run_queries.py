import duckdb
import os
import pandas as pd
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config_param import mimic_path, derive_path, derive_queries_path

def load_query(query_file_path):
    with open(query_file_path, 'r') as file:
        query = file.read()
    return query

def run_query(database_name, query_filename, output_filename, tables_to_load):
    """
    Executes a SQL query from a file and writes the result to a CSV file.
    
    Parameters:
    - database_name: The name of the database (e.g., 'ventilation.db').
    - query_filename: The SQL file that contains the query (e.g., 'bg.sql').
    - output_filename: The name of the CSV file to store the results (e.g., 'bg.csv').
    - tables_to_load: A list of tuples containing (table_name, csv_file_path).
    """
    
    db_path = os.path.join(derive_path, database_name)
    con = duckdb.connect(database=db_path)
    
    # Load each CSV file into DuckDB as specified in the tables_to_load list
    for table_name, csv_file_path in tables_to_load:
        full_csv_path = os.path.join(mimic_path, csv_file_path)
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{full_csv_path}')")
    
    # Load and execute the SQL query
    query_path = os.path.join(derive_queries_path, query_filename)
    query = load_query(query_path)

    start_time = time.time()
    con.execute(query).fetchdf()
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Execution time for {query_filename}: {execution_time:.2f} seconds")

    table_name = os.path.splitext(output_filename)[0]
    fetch_query = f"SELECT * FROM {table_name};"

    # Fetch the data and save it into a dataframe
    result_df = con.execute(fetch_query).fetchdf()
    result_csv_path = os.path.join(derive_path, output_filename)
    result_df.to_csv(result_csv_path, index=False)

    # Close the connection
    con.close()
